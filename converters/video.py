from __future__ import annotations
from pathlib import Path
from uuid import uuid4
import tempfile
import subprocess


def _run_ffmpeg(cmd: list[str]) -> None:
    try:
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        raise RuntimeError("ffmpeg no está instalado o no está en el PATH del sistema.")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg falló al procesar el video (código {e.returncode}).")


def _temp_paths(suffix_in: str, suffix_out: str) -> tuple[Path, Path]:
    temp_dir = Path(tempfile.gettempdir())
    in_path = temp_dir / f"fc_in_{uuid4().hex}{suffix_in}"
    out_path = temp_dir / f"fc_out_{uuid4().hex}{suffix_out}"
    return in_path, out_path


def mp4_to_gif(
    file_bytes: bytes,
    fps: int = 15,
    target_height: int | None = None,
) -> bytes:
    """
    Convierte un MP4 a GIF usando ffmpeg.
    """
    in_path, out_path = _temp_paths(".mp4", ".gif")

    try:
        in_path.write_bytes(file_bytes)

        if target_height:
            vf = f"fps={fps},scale=-2:{target_height}"
        else:
            # Mantener tamaño par (algunos filtros/codecs lloran con tamaños impares)
            vf = f"fps={fps},scale=trunc(iw/2)*2:trunc(ih/2)*2"

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(in_path),
            "-vf", vf,
            "-loop", "0",
            str(out_path),
        ]

        _run_ffmpeg(cmd)

        return out_path.read_bytes()

    finally:
        for p in (in_path, out_path):
            try:
                if p.exists():
                    p.unlink()
            except PermissionError:
                # Windows a veces tarda en soltar el handle. No rompemos la app por eso.
                pass


def compress_mp4_ffmpeg(
    file_bytes: bytes,
    crf: int = 28,
    target_height: int | None = 720,
) -> bytes:
    """
    Comprime un MP4 usando ffmpeg:
    - crf: calidad (18–23 buena, 28 más comprimido).
    - target_height: altura objetivo (ej: 720 -> 720p).
    """
    in_path, out_path = _temp_paths(".mp4", ".mp4")

    try:
        in_path.write_bytes(file_bytes)

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(in_path),
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", "medium",
        ]

        if target_height:
            cmd += ["-vf", f"scale=-2:{target_height}"]

        cmd += [
            "-c:a", "aac",
            "-b:a", "128k",
            str(out_path),
        ]

        _run_ffmpeg(cmd)

        return out_path.read_bytes()

    finally:
        for p in (in_path, out_path):
            try:
                if p.exists():
                    p.unlink()
            except PermissionError:
                # Si Windows no deja borrar ahora, que lo limpie solo después.
                pass