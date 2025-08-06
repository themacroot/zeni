from fastapi import APIRouter, Request
from backend.app.utils.query_optimizer import optimize_query, load_symspell, load_banking_terms

router = APIRouter()
sym_spell = load_symspell()
banking_terms = load_banking_terms()

@router.post("/query/optimize")
async def optimize_user_query(request: Request):
    payload = await request.json()
    query = payload.get("query", "")

    result = optimize_query(query, sym_spell, banking_terms)
    auto_process = result["original"].lower().strip() == result["optimized"].lower().strip()

    return {
        "original_query": result["original"],
        "optimized_query": result["optimized"],
        "auto_forward": auto_process  # True if no change detected
    }
