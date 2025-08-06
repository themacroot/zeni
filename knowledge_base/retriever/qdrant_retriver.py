from typing import List, Dict
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

# Constants
EMBEDDING_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
QDRANT_URL = "http://localhost:6333"

# Shared components
embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
qdrant_client = QdrantClient(url=QDRANT_URL)

def query_qdrant(query: str, collection_name: str, k: int = 2) -> List[Dict]:
    """
    Query Qdrant vector store for top-k relevant documents from a given collection.

    Args:
        query (str): The user query.
        collection_name (str): Name of the Qdrant collection.
        k (int): Number of relevant chunks to return.

    Returns:
        List[Dict]: A list of documents with metadata and score.
    """
    vectorstore = Qdrant(
        client=qdrant_client,
        collection_name=collection_name,
        embeddings=embedding_model,
    )

    results = vectorstore.similarity_search_with_score(query, k=k)

    documents_with_metadata = []
    for doc, score in results:
        documents_with_metadata.append({
            "text": doc.page_content,
            "metadata": doc.metadata,
            "score": score
        })

    return documents_with_metadata
