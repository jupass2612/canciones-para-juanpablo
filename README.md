# Canciones para Juan Pablo ❤️

Web app para el iPhone de Juan Pablo (también se ve bien en tableta y computadora): recibe las canciones que le dedicas, con la letra sincronizada, un mensaje tuyo escrito a mano y una canción del día que también aparece en un widget.

## Cómo funciona

- **Juan Pablo** abre la app y ve la **canción de hoy** y todas sus **dedicatorias**. No puede subir ni cambiar nada. Las nuevas aparecen marcadas como "Nueva".
- **Tú** activas en tu iPhone un modo oculto para **dedicar**: subes el audio, pegas la letra, la sincronizas tocando al ritmo, escribes tu mensaje y eliges el día. Al tocar **Dedicársela**, la app publica la canción en GitHub y a ella le llega en un par de minutos.
- **Canción del día**: si ese día le dedicaste una, es esa (con la etiqueta "Nueva"). Si no, rota entre las anteriores. Puedes programar canciones para fechas futuras (aniversario, cumpleaños): ella no las ve hasta ese día.

## 1. Publicar la app (una sola vez)

1. Crea un repositorio en GitHub llamado `canciones-para-juanpablo` y sube todo el contenido de esta carpeta.
2. En el repositorio: **Settings → Pages → Branch: main / (root) → Save**.
3. Unos minutos después queda en `https://TU-USUARIO.github.io/canciones-para-juanpablo/`.

Ojo: en un repositorio público cualquiera con el enlace puede ver la app y descargar los MP3. Si es posible, usa un repositorio privado con Pages (requiere GitHub Pro), o al menos no compartas el enlace.

## Bajar canciones con el link de YouTube (solo esta versión)

1. En **Dedicar**, pega el link de YouTube en **Link de YouTube**. La app toma el título y el artista del video y busca la portada, el álbum y la letra.
2. Toca **Dedicársela** sin elegir archivo de audio. La canción se publica como pendiente ("Bajando de YouTube…") y todavía no aparece en Hoy.
3. GitHub (pestaña **Actions → Bajar canciones de YouTube**) baja el MP3 con yt-dlp, lo guarda en `songs/`, vuelve a elegir la letra sincronizada según la duración real y deja la canción lista. Tarda de 1 a 3 minutos.
4. Si falla, en Dedicatorias → ⋯ → **Reintentar YouTube**. El motivo del error aparece en la app.

**Si YouTube bloquea a GitHub** ("confirma que no eres un robot"), puedes agregar tus cookies de YouTube:
exporta `cookies.txt` de youtube.com con una extensión como "Get cookies.txt LOCALLY" (usa una cuenta de Google secundaria, no la principal) y pégalo completo en
**Settings → Secrets and variables → Actions → New repository secret**, nombre `YT_COOKIES`. Las cookies caducan; si vuelve a fallar, repite el paso.

## 2. Activar el modo dedicar en tu iPhone (una sola vez)

1. En GitHub: **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
   - Repository access: **Only select repositories** → `canciones-para-juanpablo`.
   - Permissions → Repository permissions → **Contents: Read and write**.
   - Elige una caducidad larga (por ejemplo, 1 año).
2. En tu iPhone abre `https://TU-USUARIO.github.io/canciones-para-juanpablo/#admin`.
3. Escribe tu usuario, el repositorio y el token, y toca **Guardar y probar**. Aparece la pestaña **Dedicar**.

El token se guarda solo en tu iPhone. El iPhone de Juan Pablo nunca lo tiene, así que ella solo recibe.

## 3. Dedicar una canción

1. Pestaña **Dedicar** → título, artista y tu mensaje.
2. Elige el día en que la recibe (hoy, por defecto) y un color.
3. Audio: elige el MP3 o M4A desde la app Archivos.
4. Toca **Buscar letra**: la app la busca en LRCLIB (base de datos abierta de letras) con el título y el artista, y te muestra las versiones con su duración. Elige la que coincide con tu audio; muchas ya vienen sincronizadas. Si no aparece, pégala tú y toca **Sincronizar letra** para marcar cada verso mientras suena.
5. Si la canción está en otro idioma, elige el idioma y toca **Traducir automáticamente**. Revisa y corrige la traducción (un renglón por verso). Juan Pablo la verá debajo de cada verso y puede ocultarla con el botón **ES** del reproductor.
6. **Dedicársela**. Si no terminas, **Guardar borrador** la deja guardada en tu iPhone sin publicarla.

Desde **Dedicatorias → ⋯** puedes editar o quitar las que ya publicaste.

## 4. En el iPhone de Juan Pablo

- **Instalar la app**: abre el enlace en Safari → Compartir → **Agregar a pantalla de inicio**.
- **Escuchar sin internet**: en **Dedicatorias** puede tocar el botón de descarga de cada canción o **Descargar todas**. Las descargadas llevan una palomita y se escuchan aunque no tenga señal. Las canciones nuevas que le dedicas se descargan solas al abrir la app con internet (se puede apagar ahí mismo).
- **Widget**: instala **Scriptable** (gratis en la App Store), crea un script nuevo con el contenido de `widget/cancion-del-dia-scriptable.js`, cambia `BASE` por tu dirección y agrega un widget de Scriptable (chico o mediano) eligiendo ese script. Muestra la canción de hoy con su color y tu mensaje, dice "NUEVA PARA TI" el día que le dedicas una, y abre la app al tocarlo. iOS decide cada cuánto se actualiza (normalmente cada 15 a 60 minutos).

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | Toda la app (vista de Juan Pablo y modo dedicar) |
| `songs/songs.json` | Lista de canciones publicadas. La app la actualiza sola |
| `songs/*.mp3` | Audios que vas subiendo |
| `manifest.webmanifest`, `icons/`, `sw.js` | Instalación como app y uso sin internet |
| `widget/cancion-del-dia-scriptable.js` | Widget para el iPhone |

Para probar en tu PC: `npx serve .` y abre `http://localhost:3000`.
