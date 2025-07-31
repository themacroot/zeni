from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

# You can adjust this as per your embedding model and config
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
QDRANT_COLLECTION = "regulatory_docs"
QDRANT_URL = "http://localhost:6333"

# Initialize once and reuse
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
qdrant_client = QdrantClient(url=QDRANT_URL)

vectorstore = Qdrant(
    client=qdrant_client,
    collection_name=QDRANT_COLLECTION,
    embeddings=embedding_model,
)


def query_qdrant(query: str, k: int = 5) -> List[Dict]:
    """
    Query Qdrant vector store for top-k relevant documents.

    Args:
        query (str): The user query.
        k (int): Number of relevant chunks to return.

    Returns:
        List[Dict]: A list of documents with metadata.
    """
    results = vectorstore.similarity_search_with_score(query, k=5)

    documents_with_metadata = []
    for doc, score in results:
        documents_with_metadata.append({
            "text": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        })

    return documents_with_metadata
