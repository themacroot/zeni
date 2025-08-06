
from pydantic import BaseModel
from typing import List, Literal

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class RAGChatRequest(BaseModel):
    context: List[ChatMessage]
    chat_type: Literal["rbi", "internal", "hr", "it","faq"]
