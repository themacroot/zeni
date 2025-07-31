from fastapi import UploadFile
import io
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd

async def parse_file(file: UploadFile) -> str:
    contents = await file.read()
    ext = file.filename.split('.')[-1].lower()

    if ext == "pdf":
        reader = PdfReader(io.BytesIO(contents))
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    elif ext == "docx":
        doc = Document(io.BytesIO(contents))
        return "\n".join(p.text for p in doc.paragraphs)

    elif ext in ["xlsx", "csv"]:
        df = pd.read_excel(io.BytesIO(contents)) if ext == "xlsx" else pd.read_csv(io.BytesIO(contents))
        return df.to_string()

    return "Unsupported file"
