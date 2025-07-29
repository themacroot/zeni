from llama_cpp import Llama
from typing import List, Dict
from .base import BaseLLM
from llm_server.launcher.utils.config import settings
from llm_server.launcher.utils.logger import logger

class LlamaCppLLM(BaseLLM):
    def __init__(self):
        self.model = Llama(
            model_path=settings.model_path,
            n_ctx=settings.n_ctx,
            n_threads=settings.n_threads,
            n_gpu_layers=settings.n_gpu_layers,
            use_mlock=True,
            embedding=False
        )

    def generate_stream(self, messages: List[Dict[str, str]]):
        prompt = self.format_chat_context(messages)
        stream = self.model(prompt, max_tokens=1024, stream=True,stop=["<|user|>", "<|system|>","<|user||>", "<|assistant||>"],)
        for chunk in stream:
            yield chunk.get("choices", [{}])[0].get("text", "")


    def format_chat_context(self,messages: List[Dict[str, str]]) -> str:
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