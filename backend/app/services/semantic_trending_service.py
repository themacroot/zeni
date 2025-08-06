# backend/services/semantic_trending_service.py

from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
)
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "trending_questions"
EMBED_DIM = 384  # Based on all-MiniLM-L6-v2, change if you're using another model
DISTANCE = Distance.COSINE
QDRANT_URL = "http://localhost:6333"

# Initialize embedding model and Qdrant client
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant_client = QdrantClient(url=QDRANT_URL)


def ensure_collection_exists():
    existing = qdrant_client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in existing]:
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBED_DIM,
                distance=DISTANCE
            )
        )




# 2. Record or update a question in trending collection
def record_question(query: str, mode: str):
    ensure_collection_exists()
    embedding = model.encode(query).tolist()

    search_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        limit=1,
        score_threshold=0.50,
        query_filter=Filter(
            must=[
                FieldCondition(key="mode", match=MatchValue(value=mode)),
            ]
        )
    )

    if search_result:
        point_id = search_result[0].id
        current_freq = search_result[0].payload.get("frequency", 1)
        qdrant_client.set_payload(
            collection_name=COLLECTION_NAME,
            payload={"frequency": current_freq + 1},
            points=[point_id]
        )
    else:
        qdrant_client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "question": query,
                        "mode": mode,
                        "frequency": 1,
                        "created_at": datetime.utcnow().isoformat()
                    }
                )
            ]
        )


# 3. Get top trending questions for a given mode
def get_trending_questions(mode: str, limit: int = 10):
    result, _ = qdrant_client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[FieldCondition(key="mode", match=MatchValue(value=mode))]
        ),
        with_payload=True,
        with_vectors=False,
        limit=100  # Fetch more to sort client-side
    )

    sorted_by_freq = sorted(result, key=lambda x: x.payload.get("frequency", 0), reverse=True)
    return [
        {
            "question": point.payload.get("question"),
            "frequency": point.payload.get("frequency"),
            "last_updated": point.payload.get("created_at"),
        }
        for point in sorted_by_freq[:limit]
    ]
