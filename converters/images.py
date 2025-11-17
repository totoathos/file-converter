from io import BytesIO
from PIL import Image

def convert_image(file_bytes: bytes, target_format: str) -> bytes:
    img = Image.open(BytesIO(file_bytes))
    output = BytesIO()
    img.save(output, format=target_format.upper())
    return output.getvalue()