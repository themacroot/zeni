from pydantic import BaseModel

class RAGChatRequest(BaseModel):
    query: str
    chat_type: str  # rbi | internal | hr | it
