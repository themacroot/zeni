from typing import List, Dict, Generator
from models.cpp_backend import LlamaCppLLM
from models.vllm_backend import VLLMLLM
from llm_server.launcher.utils.config import settings


class LLMInterface:
    def __init__(self):
        backend_type = settings.model_type  # e.g., "llama.cpp" or "vllm"

        if backend_type == "llama-cpp":
            self.backend = LlamaCppLLM()
        elif backend_type == "vllm":
            self.backend = VLLMLLM()
        else:
            raise ValueError(f"Unsupported backend type: {backend_type}")

    def generate_stream(self, messages: str) -> Generator[str, None, None]:
        return self.backend.generate_stream(messages)
