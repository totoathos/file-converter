from io import BytesIO
from pydub import AudioSegment

def audio_convert(file_bytes: bytes, src_format: str, target_format: str) -> bytes:
    audio = AudioSegment.from_file(BytesIO(file_bytes), format=src_format)
    output = BytesIO()
    audio.export(output, format=target_format)
    return output.getvalue()