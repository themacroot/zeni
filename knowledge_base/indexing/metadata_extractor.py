from pathlib import Path
from datetime import datetime

def extract_metadata(file_path: Path, chunk_index: int) -> dict:
    parts = file_path.parts
    return {
        "source_path": str(file_path),
        "chunk_index": chunk_index,
        "regulator": parts[-4] if len(parts) > 3 else "unknown",
        "category": parts[-3] if len(parts) > 2 else "uncategorized",
        "subcategory": parts[-2] if len(parts) > 1 else "",
        "filename": file_path.stem,
        "file_ext": file_path.suffix,
        "ingested_at": datetime.utcnow().isoformat()
    }
