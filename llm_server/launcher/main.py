from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from config import settings
from logger import logger
from models import load_model, generate_stream
import uvicorn

app = FastAPI(title="LLM Server", version="1.0.0")

# Load the appropriate model based on config
try:
    llm = load_model(settings)
    logger.info(f"Loaded model: {settings.model_type} from {settings.model_path}")
except Exception as e:
    logger.exception("Failed to load model")
    raise e

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        messages = data.get("context", [])
        prompt = data.get("prompt", "").strip()

        if not messages:
            raise HTTPException(status_code=400, detail="Missing 'prompt' in request body")

        logger.info(f"Received prompt of length {len(messages)}")

        return StreamingResponse(generate_stream(llm, messages), media_type="text/plain")

    except Exception as e:
        logger.exception("Unhandled exception during generation")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    logger.info(f"Starting LLM server on {settings.host}:{settings.port}...")
    uvicorn.run("main:app", host=settings.host, port=settings.port, log_level="info")
