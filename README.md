# File Converter 🔁

Aplicación simple hecha en **Python + Streamlit** para convertir archivos comunes sin sufrir de más.

Permite:

- Imágenes:
  - JPG → PNG
  - PNG → WEBP
- Tablas:
  - CSV → XLSX
  - XLSX → CSV
- Audio:
  - WAV → MP3
  - MP3 → WAV
- Video:
  - MP4 → GIF
  - MP4 → MP4 comprimido (usando `ffmpeg`)

---

## Tecnologías utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/) para la interfaz web
- [Pillow](https://python-pillow.org/) para imágenes
- [pandas](https://pandas.pydata.org/) + `openpyxl` para CSV/XLSX
- [pydub](https://github.com/jiaaro/pydub) para audio
- [moviepy](https://zulko.github.io/moviepy/) para GIFs
- [`ffmpeg`](https://ffmpeg.org/) para compresión de MP4

---

## Requisitos

- Python 3.9 o superior
- `ffmpeg` instalado y disponible en el `PATH` del sistema (para:
  - compresión de MP4
  - parte de funciones de audio/video)

### Verificar `ffmpeg`

```bash
ffmpeg -version
