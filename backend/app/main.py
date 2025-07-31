from fastapi import FastAPI
from backend.app.api.routes import general_chat, rag_chat
from backend.app.core.middleware import setup_middlewares

app = FastAPI(title="Zeni AI")

setup_middlewares(app)

app.include_router(general_chat.router, prefix="/chat/general", tags=["General Chat"])
app.include_router(rag_chat.router, prefix="/chat/rag", tags=["RAG Chat"])

