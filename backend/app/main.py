from fastapi import FastAPI
from backend.app.api.routes import general_chat, rag_chat, trending
from backend.app.core.middleware import setup_middlewares
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Zeni AI")


# Allow frontend origin
origins = [
    "http://localhost:8080",  # or wherever your frontend is hosted
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # allow all: ["*"] for dev, restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



setup_middlewares(app)

app.include_router(general_chat.router, prefix="/chat/general", tags=["General Chat"])
app.include_router(rag_chat.router, prefix="/chat/rag", tags=["RAG Chat"])

app.include_router(trending.router, prefix="/trending/{mode}", tags=["Trending Chat"])
