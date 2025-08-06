# knowledge_base/indexing/symspell_dictionary_builder.py

import re
import unicodedata
from pathlib import Path
from collections import Counter
from knowledge_base.indexing.loader_factory import load_document_text

def tokenize(text: str):
    # Remove hyphenation at line breaks
    text = re.sub(r'-\s*\n\s*', '', text)
    # Replace newlines with spaces
    text = text.replace('\n', ' ')
    # Normalize unicode characters to ASCII
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Only alphabetic words of length >=2
    return re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

def build_word_frequency_dict_from_directory(resource_dir: Path) -> Counter:
    word_counter = Counter()
    for file_path in resource_dir.rglob("*.*"):
        try:
            content = load_document_text(file_path)
            words = tokenize(content)
            word_counter.update(words)
        except Exception as e:
            print(f"Skipping {file_path} due to error: {e}")
    return word_counter

def save_symspell_dictionary(counter: Counter, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        for word, freq in counter.items():
            if freq >= 15:
                f.write(f"{word} {freq}\n")

if __name__ == "__main__":
    base_dir = Path("../resource")  # Your actual document root
    output_file = Path("../resource/custom_symspell_dictionary.txt")

    print(f"Building dictionary from: {base_dir}")
    counter = build_word_frequency_dict_from_directory(base_dir)
    save_symspell_dictionary(counter, output_file)

    print(f"✅ Dictionary created at: {output_file}")
