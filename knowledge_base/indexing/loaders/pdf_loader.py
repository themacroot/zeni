from PyPDF2 import PdfReader

def load_pdf(file_path):
    text = ""
    try:
        reader = PdfReader(str(file_path))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"[PDFLoader] Error reading {file_path}: {e}")
    return text
