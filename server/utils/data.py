import pandas as pd
from fastapi import UploadFile
import io

async def load_csv_data(file: UploadFile) -> pd.DataFrame:
    """
    Reads and parses a CSV file uploaded by the user.

    Returns:
    - pandas DataFrame
    """
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content), encoding="utf-8")
        df.columns = df.columns.str.strip()  # Optional: clean column names
        return df
    except UnicodeDecodeError:
        raise ValueError("File encoding is not UTF-8. Please upload a UTF-8 encoded CSV.")
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {str(e)}")
