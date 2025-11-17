import streamlit as st
from converters.images import convert_image
from converters.tables import csv_to_xlsx, xlsx_to_csv
from converters.audio import audio_convert
from converters.video import mp4_to_gif, compress_mp4_ffmpeg

st.set_page_config(page_title="Mini File Converter")

MODES = {
    "JPG a PNG": "img_jpg_png",
    "PNG a WEBP": "img_png_webp",
    "CSV a XLSX": "csv_xlsx",
    "XLSX a CSV": "xlsx_csv",
    "WAV a MP3": "wav_mp3",
    "MP3 a WAV": "mp3_wav",
    "MP4 a GIF": "mp4_gif",
    "MP4 Comprimir (con ffmpeg)": "mp4_compress",
}

st.title("File Converter")

mode_label = st.selectbox("Tipo de conversión", list(MODES.keys()))
mode = MODES[mode_label]

uploaded = st.file_uploader("Subí el archivo", type=None)

if uploaded and st.button("Convertir"):
    file_bytes = uploaded.read()
    result_bytes = None
    out_name = None

    base_name = uploaded.name.rsplit(".", 1)[0]

    if mode == "img_jpg_png":
        result_bytes = convert_image(file_bytes, "PNG")
        out_name = base_name + ".png"

    elif mode == "img_png_webp":
        result_bytes = convert_image(file_bytes, "WEBP")
        out_name = base_name + ".webp"

    elif mode == "csv_xlsx":
        result_bytes = csv_to_xlsx(file_bytes)
        out_name = base_name + ".xlsx"

    elif mode == "xlsx_csv":
        result_bytes = xlsx_to_csv(file_bytes)
        out_name = base_name + ".csv"

    elif mode == "wav_mp3":
        result_bytes = audio_convert(file_bytes, "wav", "mp3")
        out_name = base_name + ".mp3"

    elif mode == "mp3_wav":
        result_bytes = audio_convert(file_bytes, "mp3", "wav")
        out_name = base_name + ".wav"

    elif mode == "mp4_gif":
        result_bytes = mp4_to_gif(file_bytes)
        out_name = base_name + ".gif"

    elif mode == "mp4_compress":
        try:
            # CRF y resolución por defecto adentro de compress_mp4_ffmpeg
            result_bytes = compress_mp4_ffmpeg(file_bytes)
            out_name = base_name + "_compressed.mp4"
        except FileNotFoundError:
            st.error("ffmpeg no está instalado o no está en el PATH del sistema.")
        except Exception as e:
            st.error(f"Ocurrió un error al comprimir el video: {e}")

    if result_bytes:
        st.success("Conversión completa.")
        st.download_button(
            "Descargar archivo convertido",
            data=result_bytes,
            file_name=out_name
        )
