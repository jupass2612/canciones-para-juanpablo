# Baja de YouTube las canciones pendientes (las que publicaste con link de YouTube y sin MP3).
# Lo ejecuta GitHub Actions: .github/workflows/youtube.yml
import json, os, re, subprocess, sys, urllib.parse, urllib.request

SONGS = "songs/songs.json"
BRANCH = os.environ.get("BRANCH") or "main"


def load():
    with open(SONGS, encoding="utf-8") as f:
        j = json.load(f)
    return j


def songs_of(j):
    return j if isinstance(j, list) else j.get("songs", [])


def save(j):
    with open(SONGS, "w", encoding="utf-8") as f:
        f.write(json.dumps(j if isinstance(j, dict) else {"songs": j}, ensure_ascii=False, indent=2) + "\n")


def sh(*args, check=True):
    return subprocess.run(args, check=check, capture_output=True, text=True)


def clean(msg):
    msg = re.sub(r"\x1b\[[0-9;]*m", "", str(msg)).replace("ERROR: ", "").strip()
    low = msg.lower()
    if "not a bot" in low or "sign in to confirm" in low:
        return "YouTube pidió confirmar que no es un robot (bloqueó a GitHub). Prueba de nuevo más tarde o agrega el secreto YT_COOKIES"
    if "private" in low:
        return "el video es privado"
    if "unavailable" in low or "not available" in low:
        return "el video no está disponible"
    if "age" in low and "confirm" in low:
        return "el video pide confirmar la edad; agrega el secreto YT_COOKIES"
    return msg[:220]


def lrclib(title, artist, dur):
    """Busca la letra sincronizada cuya duración coincide (±3 s) con el audio que se bajó."""
    if not title or not dur:
        return None
    q = {"track_name": title}
    if artist:
        q["artist_name"] = re.split(r",| ft\.? | feat\.? | & | x | y ", artist, flags=re.I)[0].strip()
    req = urllib.request.Request("https://lrclib.net/api/search?" + urllib.parse.urlencode(q),
                                 headers={"User-Agent": "canciones-app (github actions)"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            items = json.load(r)
    except Exception as e:
        print("  No pude buscar la letra:", e)
        return None
    best = sorted((x for x in items if x.get("syncedLyrics") and x.get("duration")),
                  key=lambda x: abs(x["duration"] - dur))
    if best and abs(best[0]["duration"] - dur) <= 3:
        print(f"  Letra sincronizada que dura {best[0]['duration']:.0f} s (el audio dura {dur:.0f} s)")
        return best[0]["syncedLyrics"].strip()
    return None


def download(sid, url):
    import yt_dlp
    out = f"songs/{sid}"
    opts = {
        "format": "bestaudio/best",
        "outtmpl": out + ".%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "retries": 3,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "0"},
            {"key": "FFmpegMetadata"},
        ],
    }
    if os.environ.get("YT_COOKIES"):
        with open("/tmp/cookies.txt", "w") as f:
            f.write(os.environ["YT_COOKIES"])
        opts["cookiefile"] = "/tmp/cookies.txt"
    with yt_dlp.YoutubeDL(opts) as y:
        info = y.extract_info(url, download=True)
    path = out + ".mp3"
    if not os.path.exists(path):
        raise RuntimeError("no se generó el MP3")
    if os.path.getsize(path) > 95 * 1024 * 1024:
        os.remove(path)
        raise RuntimeError("el audio pesa más de 95 MB (GitHub no acepta archivos tan grandes)")
    return path, info


pending = [s for s in songs_of(load()) if s.get("ytPending") and s.get("yt")]
if not pending:
    print("No hay canciones pendientes.")
    sys.exit(0)

results = {}
for s in pending:
    sid, url = s["id"], s["yt"]
    print(f"Bajando: {s.get('title')} — {url}")
    try:
        path, info = download(sid, url)
        dur = info.get("duration")
        up = {"audio": path, "ytPending": None, "ytError": None, "ytFix": None,
              "duration": round(dur) if dur else None}
        lyr = s.get("lyrics") or ""
        if s.get("ytFix") or not re.search(r"\[\d+:\d+", lyr):
            new = lrclib(s.get("title"), s.get("artist"), dur)
            if new:
                up["lyrics"] = new
        results[sid] = {"url": url, "up": up, "file": path}
        print(f"  Listo ({os.path.getsize(path) / 1e6:.1f} MB)")
    except Exception as e:
        err = clean(e)
        print("  No se pudo:", err)
        results[sid] = {"url": url, "up": {"ytPending": None, "ytError": err}, "file": None}

sh("git", "config", "user.name", "github-actions[bot]")
sh("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

ok = False
for attempt in range(5):
    # Toma la lista más nueva (por si publicaste otra canción mientras se bajaba) y aplica los cambios.
    sh("git", "fetch", "origin", BRANCH)
    sh("git", "reset", "--hard", f"origin/{BRANCH}")  # los MP3 nuevos no se borran (no están en git todavía)
    j = load()
    files = [SONGS]
    for s in songs_of(j):
        r = results.get(s.get("id"))
        if not r or not s.get("ytPending") or s.get("yt") != r["url"]:
            continue  # la cambiaste mientras tanto: se baja en la siguiente vuelta
        for k, v in r["up"].items():
            if v is None:
                s.pop(k, None)
            else:
                s[k] = v
        if r["file"]:
            files.append(r["file"])
    save(j)
    sh("git", "add", *files)
    if sh("git", "diff", "--cached", "--quiet", check=False).returncode == 0:
        print("Nada que guardar.")
        ok = True
        break
    sh("git", "commit", "-m", "Canciones bajadas de YouTube")
    if sh("git", "push", "origin", f"HEAD:{BRANCH}", check=False).returncode == 0:
        ok = True
        break
    print("Alguien guardó cambios al mismo tiempo; reintento…")

if not ok:
    print("No pude guardar los cambios en el repo.")
    sys.exit(1)

if any(r["file"] for r in results.values()):
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    # Publica la página otra vez y manda el aviso de canción nueva (si los avisos están configurados).
    sh("gh", "api", "-X", "POST", f"repos/{repo}/pages/builds", check=False)
    if os.path.exists(".github/workflows/avisos.yml"):
        r = sh("gh", "workflow", "run", "avisos.yml", "--ref", BRANCH, "-f", "motivo=youtube", check=False)
        print("Aviso:", "pedido" if r.returncode == 0 else r.stderr.strip())

if any(not r["file"] for r in results.values()):
    print("Algunas canciones no se pudieron bajar; en la app aparece el motivo.")
