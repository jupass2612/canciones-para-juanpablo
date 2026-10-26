# Mi música

Mi reproductor personal: letras sincronizadas, canción del día, widget para el iPhone, descargas para escuchar sin internet y canciones que se bajan solas con el link de YouTube.

## 1. Publicarla (una sola vez)

1. Crea un repositorio en GitHub llamado `canciones-para-juanpablo` y sube todo el contenido de esta carpeta.
   La carpeta `.github` hay que crearla a mano con **Add file → Create new file** (escribe la ruta completa, por ejemplo `.github/workflows/youtube.yml`, y pega el contenido).
2. **Settings → Pages → Branch: main / (root) → Save**.
3. Queda en `https://TU-USUARIO.github.io/canciones-para-juanpablo/`.

En un repositorio público cualquiera con el enlace puede abrir la app y bajar los MP3. No compartas el enlace.

## 2. Modo administrador en tu iPhone (una sola vez)

1. GitHub: **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
   - Repository access: **Only select repositories** → `canciones-para-juanpablo`.
   - Permissions → Repository permissions → **Contents: Read and write**.
2. Abre `https://TU-USUARIO.github.io/canciones-para-juanpablo/#admin`, escribe tu usuario, el repositorio y el token, y toca **Guardar y probar**. Aparece la pestaña **Agregar**.

## 3. Agregar canciones

- **Con link de YouTube**: pégalo en **Link de YouTube**. La app toma el título y el artista del video y busca portada, álbum y letra. Toca **Guardar canción** sin elegir audio.
  La canción queda como "Bajando de YouTube…" y GitHub (pestaña **Actions → Bajar canciones de YouTube**) baja el MP3, lo guarda en `songs/` y vuelve a elegir la letra sincronizada según la duración real. Tarda de 1 a 3 minutos.
  Si falla, en **Biblioteca → ⋯ → Reintentar YouTube**. El motivo aparece en la app.
- **Con archivo**: elige el MP3 o M4A en **Audio**, como siempre.
- **Letra**: se busca sola. Si no aparece, pégala y toca **Sincronizar letra** (tocas cada vez que empieza un verso).

**Si YouTube bloquea a GitHub** ("confirma que no eres un robot"): exporta `cookies.txt` de youtube.com con la extensión "Get cookies.txt LOCALLY" (mejor con una cuenta de Google secundaria) y pégalo en **Settings → Secrets and variables → Actions → New repository secret** con el nombre `YT_COOKIES`. Las cookies caducan; si vuelve a fallar, repítelo.

## 4. En el iPhone

- **Instalar**: Safari → Compartir → **Agregar a pantalla de inicio**.
- **Sin internet**: en **Biblioteca** toca el botón de descarga de cada canción o **Descargar todas**.
- **Avisos (opcional)**: agrega el secreto `VAPID_PRIVATE_KEY` en el repo, toca **Activar avisos** en la app y pega el código en Ajustes. Te avisa cuando una canción termina de bajarse.
- **Widget**: instala **Scriptable**, crea un script con `widget/cancion-del-dia-scriptable.js`, cambia `BASE` por tu dirección y agrega el widget.

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | Toda la app |
| `songs/songs.json` | Lista de canciones. La app la actualiza sola |
| `songs/*.mp3` | Audios (los que subes y los que baja GitHub) |
| `.github/workflows/youtube.yml`, `.github/scripts/youtube.py` | Bajan las canciones de YouTube |
| `.github/workflows/avisos.yml`, `.github/scripts/avisos.mjs` | Avisos al celular |
| `manifest.webmanifest`, `icons/`, `sw.js` | Instalación como app y uso sin internet |
| `widget/cancion-del-dia-scriptable.js` | Widget para el iPhone |
