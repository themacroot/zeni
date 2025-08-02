# backend/app/services/llm_service.py
import httpx
from typing import List, Dict
from backend.app.utils.chat_formatter import format_chat_with_roles

async def call_llm(messages: List[Dict[str, str]]) -> str:
    formatted_prompt = format_chat_with_roles(messages)

    payload = {
        "prompt": formatted_prompt
    }

    async with httpx.AsyncClient() as client:
        try:
            print(payload)
            response = await client.post("http://localhost:8001/generate", json=payload, timeout=400)
            response.raise_for_status()
            print(response.content)
            return response.content.decode('utf-8')

        except httpx.RequestError as exc:
            return f"⚠️ HTTP error: {exc}"
        except httpx.HTTPStatusError as exc:
            return f"⚠️ LLM server returned an error: {exc.response.status_code}"
        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"
