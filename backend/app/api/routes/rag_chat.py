from fastapi import APIRouter
from backend.app.models.chat import RAGChatRequest
from backend.app.services.rag_service import run_rag_pipeline

router = APIRouter()

@router.post("/")
async def rag_chat(payload: RAGChatRequest):
    answer = await run_rag_pipeline(payload.query, payload.chat_type)
    return {"response": answer}
