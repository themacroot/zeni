from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from llm_server.launcher.utils.config import settings
from llm_server.launcher.utils.logger import logger
from llm_interface import LLMInterface
import uvicorn

app = FastAPI(title="LLM Server", version="1.0.0")

# Load LLM interface (which internally picks the correct backend)
try:
    llm = LLMInterface()
    logger.info(f"Loaded backend: {settings.model_type} using model: {settings.model_path}")
except Exception as e:
    logger.exception("Failed to initialize LLM interface")
    raise e

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        messages = data.get("context", [])

        if not messages:
            raise HTTPException(status_code=400, detail="Missing 'context' in request body")

        logger.info(f"Received context with {len(messages)} messages")

        return StreamingResponse(llm.generate_stream(messages), media_type="text/plain")

    except Exception as e:
        logger.exception("Unhandled exception during generation")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting LLM server on {settings.host}:{settings.port}...")
    uvicorn.run("main:app", host=settings.host, port=settings.port, log_level="info")
