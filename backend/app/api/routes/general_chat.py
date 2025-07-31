from fastapi import APIRouter, File, UploadFile, Form
from backend.app.services.llm_service import call_llm
from backend.app.services.file_processor import parse_file

router = APIRouter()

@router.post("/")
async def general_chat(
    query: str = Form(...),
    file: UploadFile = File(None)
):
    content = ""
    if file:
        content = await parse_file(file)

    input_text = f"{content}\n\nUser Query: {query}" if content else query
    response = await call_llm(input_text)
    return {"response": response}
