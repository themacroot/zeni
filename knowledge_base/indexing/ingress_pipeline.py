from pathlib import Path
from typing import Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

from knowledge_base.indexing.loader_factory import load_document_text
from knowledge_base.indexing.metadata_extractor import extract_metadata
from knowledge_base.indexing.file_hash_tracker import FileHashTracker
from knowledge_base.indexing.chunker import Chunker
from knowledge_base.indexing.qdrant_uploader import QdrantUploader

def ingest_folder_to_qdrant(
    root_dir: Path,
    qdrant_url: str,
    qdrant_collection: str,
    embedding_model_name: str = "sentence-transformers/all-mpnet-base-v2",
    cache_file: Path = Path("../resource/hashes.json"),
    batch_mode: bool = True
):
    embedder = HuggingFaceEmbeddings(model_name=embedding_model_name)
    qclient = QdrantClient(url=qdrant_url)
    chunker = Chunker()
    uploader = QdrantUploader(embedder, qclient, qdrant_collection)
    hash_tracker = FileHashTracker(cache_file)

    if batch_mode:
        uploader.recreate_collection()
        existing_hashes = {}
    else:
        existing_hashes = hash_tracker.load_hashes()

    updated_hashes: Dict[str, str] = existing_hashes.copy()
    SKIP_FILES = {"hashes.json", ".DS_Store"}
    new_docs_found = False

    for file_path in root_dir.rglob("*.*"):
        if file_path.name in SKIP_FILES:
            continue
        if file_path.suffix.lower() not in [".pdf", ".docx", ".txt", ".jpg", ".png", ".xlsx"]:
            continue

        file_hash = hash_tracker.compute_file_hash(file_path)
        if not batch_mode and existing_hashes.get(str(file_path)) == file_hash:
            continue

        try:
            print("✅ Processing file", file_path)
            text = load_document_text(file_path)
            chunks = chunker.split(text)

            if not chunks:
                print(f"[WARN] No content extracted from {file_path}")
                continue

            documents = []
            metadatas = []
            for idx, chunk in enumerate(chunks):
                documents.append(chunk)
                metadatas.append(extract_metadata(file_path, idx))

            uploader.upload(documents, metadatas)
            updated_hashes[str(file_path)] = file_hash
            new_docs_found = True
        except Exception as e:
            print(f"[WARN] Failed to process {file_path}: {e}")

    if new_docs_found:
        print("✅ Ingestion complete.")
    else:
        print("ℹ️ No new documents to ingest.")

    hash_tracker.save_hashes(updated_hashes)

if __name__ == "__main__":
    ingest_folder_to_qdrant(
        root_dir=Path("../resource/"),
        qdrant_url="http://localhost:6333",
        qdrant_collection="faq",
        batch_mode=False,
    )
