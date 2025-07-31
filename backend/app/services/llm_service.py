import httpx
from typing import List, Dict

async def call_llm(prompt: str) -> str:
    payload = {
        "context": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8001/generate",
                json=payload,
                timeout=400  # optional: set timeout for production safety
            )
            response.raise_for_status()  # will raise if 4xx or 5xx

            data = response.json()
            print(response)
            return data.get("response", "⚠️ No response from LLM")

        except httpx.RequestError as exc:
            return f"⚠️ HTTP error: {exc}"

        except httpx.HTTPStatusError as exc:
            return f"⚠️ LLM server returned an error: {exc.response.status_code}"

        except Exception as e:
            return f"⚠️ Unexpected error: {str(e)}"
