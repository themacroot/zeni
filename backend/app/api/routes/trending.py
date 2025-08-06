# backend/api/routes/trending.py

from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import List

from backend.app.services.semantic_trending_service import (
    record_question,
    get_trending_questions,
)

router = APIRouter()


class QuestionInput(BaseModel):
    query: str
    mode: str


def record_trending_question(payload: QuestionInput):
    record_question(query=payload.query, mode=payload.mode)
    return {"status": "recorded"}


@router.get("")
def get_trending(mode: str, limit: int = Query(default=10, le=50)) -> List[dict]:
    return get_trending_questions(mode=mode, limit=limit)
