from pathlib import Path


def load_txt(file_path):
    try:
        return Path(file_path).read_text(encoding='utf-8')
    except Exception as e:
        print(f"[TxtLoader] Error reading {file_path}: {e}")
        return ""
