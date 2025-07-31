from knowledge_base.retriever.qdrant_retriver import query_qdrant
from backend.app.services.llm_service import call_llm

COLLECTION_MAP = {
    "rbi": "rbi_circulars",
    "internal": "internal_docs",
    "hr": "hr_docs",
    "it": "it_support_docs"
}

async def run_rag_pipeline(query: str, chat_type: str) -> str:
    collection = COLLECTION_MAP.get(chat_type)
    if not collection:
        return "Invalid chat type"

    context_chunks = query_qdrant(query, collection)
    context = "\n\n".join(chunk.get("page_content", "") for chunk in context_chunks)


    prompt = f"Context:\n{context}\n\nUser Query: {query}"

    return await call_llm(prompt)
