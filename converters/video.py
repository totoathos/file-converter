from pathlib import Path
import tempfile
import subprocess

def mp4_to_gif(file_bytes: bytes, fps: int = 15, target_height: int | None = None) -> bytes:
    """
    Convierte un MP4 a GIF usando ffmpeg para evitar dependencia de moviepy.
    - fps: cuadros por segundo del GIF resultante.
    - target_height: si se especifica, escala la altura manteniendo proporción.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        in_path = tmpdir / "input.mp4"
        out_path = tmpdir / "output.gif"

        in_path.write_bytes(file_bytes)

        if target_height:
            vf = f"fps={fps},scale=-2:{target_height}"
        else:
            # Asegura dimensiones pares necesarias para algunos códecs/convertidores
            vf = f"fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2"

        cmd = [
            "ffmpeg",
            "-y",               # overwrite
            "-i", str(in_path),
            "-vf", vf,
            "-loop", "0",
            str(out_path),
        ]

        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return out_path.read_bytes()
    

def compress_mp4_ffmpeg(
    file_bytes: bytes,
    crf: int = 28,
    target_height: int = 720,
) -> bytes:
    """
    Comprime un MP4 usando ffmpeg:
    - CRF: calidad (18 = casi sin pérdida, 28 = bastante comprimido)
    - target_height: altura del video (ej: 720 -> 720p). El ancho se ajusta solo.
    """

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        in_path = tmpdir_path / "input.mp4"
        out_path = tmpdir_path / "output.mp4"

        # Guardar input
        in_path.write_bytes(file_bytes)

        # Comando ffmpeg
        cmd = [
            "ffmpeg",
            "-y",              # overwrite
            "-i", str(in_path),
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", "medium",
        ]

        if target_height:
            # Mantiene proporción, ajusta ancho automáticamente
            cmd += ["-vf", f"scale=-2:{target_height}"]

        cmd += [
            "-c:a", "aac",
            "-b:a", "128k",
            str(out_path),
        ]

        # Ejecutar ffmpeg
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return out_path.read_bytes()