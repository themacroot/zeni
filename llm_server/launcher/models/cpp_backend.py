import json

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



    def generate_stream(self, messages: str):


        stream = self.model(messages, max_tokens=1024, stream=True,stop=["<|user|>", "<|system|>","<|user||>", "<|assistant||>"],)
        for chunk in stream:
            yield chunk.get("choices", [{}])[0].get("text", "")
