# knowledge_base/loaders/excel_loader.py

from pathlib import Path
import pandas as pd


def load_excel(file_path):
    try:
        xls = pd.ExcelFile(file_path)
        combined_content = ""

        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name)
            content = df.to_string(index=False)
            combined_content += f"\n\nSheet: {sheet_name}\n{content}"

        return combined_content.strip()

    except Exception as e:
        raise RuntimeError(f"[ExcelLoader] Error loading {file_path}: {e}")