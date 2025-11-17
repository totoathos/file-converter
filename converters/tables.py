from io import BytesIO
import pandas as pd

def csv_to_xlsx(file_bytes: bytes) -> bytes:
    df = pd.read_csv(BytesIO(file_bytes))
    output = BytesIO()
    df.to_excel(output, index=False)
    return output.getvalue()

def xlsx_to_csv(file_bytes: bytes) -> bytes:
    df = pd.read_excel(BytesIO(file_bytes))
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()