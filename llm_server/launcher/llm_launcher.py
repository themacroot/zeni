from llama_cpp import Llama
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
import logging
import os

# ---------------------------
# CONFIGURATION
# ---------------------------
MODEL_PATH = os.getenv("MODEL_PATH", "/Users/sibl15027/Projects/zeni/llm_server/quantized_models/Llama-3.1-8B-Instruct-Q4_K_M.gguf")
MAX_TOKENS = 512
MAX_PROMPT_LENGTH = 4000
N_GPU_LAYERS = 35
N_THREADS = 12
N_CTX = 4096

# ---------------------------
# LOGGING
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("llama_server")

# ---------------------------
# LOAD MODEL
# ---------------------------
logger.info("Loading LLaMA models from: %s", MODEL_PATH)
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=N_CTX,
        n_threads=N_THREADS,
        n_gpu_layers=N_GPU_LAYERS
    )
except Exception as e:
    logger.error("Failed to load LLaMA models: %s", e)
    raise

logger.info("Model loaded successfully with GPU offloading of %d layers", N_GPU_LAYERS)

# ---------------------------
# FASTAPI APP
# ---------------------------
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/generate")
async def generate(request: Request):
    try:
        data = await request.json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            raise HTTPException(status_code=400, detail="Missing 'prompt' in request")

        if len(prompt) > MAX_PROMPT_LENGTH:
            raise HTTPException(status_code=400, detail=f"Prompt too long (max {MAX_PROMPT_LENGTH} chars)")

        # Format prompt using LLaMA-style chat format (if needed)
        formatted_prompt = f"[INST] {prompt} [/INST]"

        logger.info("Generating response for prompt: %s", prompt[:100])

        output = llm(
            prompt=formatted_prompt,
            max_tokens=MAX_TOKENS,
            temperature=0.7,
            top_p=0.9,
            stop=["</s>"]
        )

        response_text = output["choices"][0]["text"].strip()
        return JSONResponse(content={"response": response_text})

    except HTTPException as e:
        raise e

    except Exception as e:
        logger.exception("Unhandled error during generation")
        return JSONResponse(status_code=500, content={"error": str(e)})

# ---------------------------
# ENTRY POINT
# ---------------------------
if __name__ == "__main__":
    logger.info("Launching LLaMA inference server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
