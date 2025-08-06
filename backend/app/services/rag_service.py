# app/services/rag_pipeline.py
from typing import List, Dict
from knowledge_base.retriever.qdrant_retriver import query_qdrant
from backend.app.services.llm_service import call_llm
from backend.app.models.chat import ChatMessage
from backend.app.services.semantic_trending_service import record_question


COLLECTION_MAP = {
    "rbi": "regulatory_docs",
    "internal": "internal_docs",
    "hr": "hr_docs",
    "it": "it_support_docs",
    "faq": "faq",
}

async def run_rag_pipeline(context: List[Dict[str, str]], chat_type: str) -> str:
    collection = COLLECTION_MAP.get(chat_type.lower())
    if not collection:
        return "⚠️ Invalid chat type"

    # Extract latest user query (last role="user")
    user_messages = [m for m in context if m.role == "user"]
    if not user_messages:
        return "⚠️ No user query found in context"

    latest_user_query = user_messages[-1].content

    record_question(latest_user_query, chat_type.lower())

    print(f"user_message",latest_user_query)
    print(f"colelction",collection)
    # Get relevant context from Qdrant
    rag_chunks = query_qdrant(latest_user_query, collection)

    print(f"rag_chunks",rag_chunks)

    rag_context = "\n\n".join(
        f"[Source: {chunk.get('metadata', {}).get('filename', 'unknown')}]\n{chunk.get('text', '')}"
        for chunk in rag_chunks
    )

    # Rewrite latest user message with RAG context
    modified_context = context.copy()
    modified_context[-1] = ChatMessage(
        role="user",
        content=f"Context:\n{rag_context}\n\nUser Query: {latest_user_query}"
    )

    # Pass updated message list to LLM
    llm_response = await call_llm(modified_context)

    references = [
        {
            "title": chunk["metadata"].get("filename", "Untitled"),
            "source": chunk["metadata"].get("subcategory", "Unknown"),
            "sourceText": chunk["text"],
            "score": chunk.get("score")
        }
        for chunk in rag_chunks
    ]

    return {
        "answer": llm_response,
        "references": references
    }