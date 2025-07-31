# knowledge_base/indexing/file_hash_tracker.py

import hashlib
import json
import os
from pathlib import Path

class FileHashTracker:
    def __init__(self, cache_file: Path):
        self.cache_file = cache_file
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)

        self._hashes = {}

    def compute_file_hash(self, file_path: Path) -> str:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def load_hashes(self) -> dict:
        if self.cache_file.exists():
            with open(self.cache_file, "r") as f:
                self._hashes = json.load(f)
        return self._hashes

    def save_hashes(self, hashes: dict):
        with open(self.cache_file, "w") as f:
            json.dump(hashes, f, indent=2)
