# knowledge_base/indexing/qdrant_uploader.py

import uuid
from typing import List
from qdrant_client import QdrantClient
from langchain_community.embeddings import HuggingFaceEmbeddings as Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client.http.models import VectorParams, Distance


class QdrantUploader:
    def __init__(self, embedder: Embeddings, client: QdrantClient, collection_name: str):
        self.embedder = embedder
        self.client = client
        self.collection_name = collection_name

    def recreate_collection(self):
        try:
            self.client.delete_collection(collection_name=self.collection_name)
        except Exception:
            pass
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"size": self.embedder.embedding_size, "distance": "Cosine"}
        )

    def upload(self, documents: List[str], metadatas: List[dict]):
        collection_name = self.collection_name
        if collection_name not in [c.name for c in self.client.get_collections().collections]:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),  # Update to your embedding size
            )

        vectorstore = Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embedder
        )
        vectorstore.add_texts(texts=documents, metadatas=metadatas, ids=[str(uuid.uuid4()) for _ in documents])
