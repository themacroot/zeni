from docx import Document

def load_docx(file_path):
    text = ""
    try:
        doc = Document(str(file_path))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"[DocxLoader] Error reading {file_path}: {e}")
    return text
