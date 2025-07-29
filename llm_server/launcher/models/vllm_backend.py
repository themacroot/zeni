import requests
from typing import List, Dict, Generator
from .base import BaseLLM
from llm_server.launcher.utils.config import Settings
from llm_server.launcher.utils.logger import logger

class VLLMLLM(BaseLLM):
    def __init__(self):
        self.api_url = f"{Settings.api_base_url}/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {Settings.api_key}",
            "Content-Type": "application/json"
        }
        self.system_prompt = {
            "role": "system",
            "content": "You are a professional assistant helping with enterprise-grade tasks. Be concise, formal, and knowledgeable."
        }

    def format_chat_context(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        all_messages = [self.system_prompt] + messages
        logger.info(f"System attached prompt is {all_messages}")
        return all_messages

    def generate_stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        payload = {
            "model": Settings.model_path,  # In vLLM, this might be like "meta-llama/Meta-Llama-3-8B-Instruct"
            "messages": self.format_chat_context(messages),
            "stream": True,
            "max_tokens": 1024,
        }

        try:
            with requests.post(self.api_url, json=payload, headers=self.headers, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        if line.startswith(b"data: "):
                            line = line[6:]
                        try:
                            chunk = line.decode("utf-8")
                            yield chunk
                        except Exception as e:
                            logger.error(f"Failed to decode stream chunk: {e}")
                            continue
        except Exception as e:
            logger.error(f"Streaming error from vLLM: {e}")
