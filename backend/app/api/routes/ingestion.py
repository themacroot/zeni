from fastapi import APIRouter
from knowledge_base.indexing.ingress_pipeline import ingest_folder_to_qdrant
from pathlib import Path

router = APIRouter()

@router.post("/ingest")
def trigger_ingestion(batch_mode: bool = False):
    ingest_folder_to_qdrant(
        root_dir=Path("knowledge_base/resource/"),
        qdrant_url="http://localhost:6333",
        qdrant_collection="regulatory_docs",
        batch_mode=batch_mode,
    )
    return {"status": "Ingestion triggered."}
