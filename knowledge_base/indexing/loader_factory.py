from pathlib import Path

from knowledge_base.indexing.loaders.pdf_loader import load_pdf
from knowledge_base.indexing.loaders.docx_loader import load_docx
from knowledge_base.indexing.loaders.txt_loader import load_txt
from knowledge_base.indexing.loaders.image_loader import load_image
from knowledge_base.indexing.loaders.excel_loader import load_excel

def load_document_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(file_path)
    elif suffix == ".docx":
        return load_docx(file_path)
    elif suffix in [".jpg", ".jpeg", ".png"]:
        return load_image(file_path)
    elif suffix == ".txt":
        return load_txt(file_path)
    elif suffix == ".xlsx":
        return load_excel(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
