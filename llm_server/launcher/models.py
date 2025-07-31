from llama_cpp import Llama
from llm_server.launcher.utils.config import Settings
from typing import Generator, List, Dict
from llm_server.launcher.utils.logger import logger

def load_model(settings: Settings):
    if settings.model_type == "llama-cpp":
        return Llama(
            model_path=settings.model_path,
            n_ctx=settings.n_ctx,
            n_threads=settings.n_threads,
            n_gpu_layers=settings.n_gpu_layers,
            use_mlock=True,
            embedding=False
        )
    else:
        raise ValueError(f"Unsupported model type: {settings.model_type}")

def format_chat_context(messages: List[Dict[str, str]]) -> str:
    system_prompt = {
        "role": "system",
        "content": "You are a professional assistant helping with enterprise-grade tasks. Be concise, formal, and knowledgeable."
    }
    all_messages = [system_prompt] + messages
    logger.info(f"Sys attached prompt is {all_messages}")
    formatted = ""
    for msg in all_messages:
        role = msg["role"]
        content = msg["content"]
        if role == "system":
            formatted += f"<|system|>\n{content}\n"
        elif role == "user":
            formatted += f"<|user|>\n{content}\n"
        elif role == "assistant":
            formatted += f"<|assistant|>\n{content}\n"

    formatted += "<|assistant|>\n"  # prompt the model to respond
    return formatted

def generate_stream(llm,messages: List[Dict[str, str]]) -> Generator[str, None, None]:
    prompt = format_chat_context(messages)
    logger.info(f"Formatted prompt is {prompt}")

    stream = llm(
        prompt,
        max_tokens=1024,
        stream=True,
        stop=["<|user|>", "<|system|>","<|user||>", "<|assistant||>"],
    )
    for chunk in stream:
        yield chunk.get("choices", [{}])[0].get("text", "")
