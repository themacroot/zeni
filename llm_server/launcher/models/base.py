from typing import List, Dict, Generator

class BaseLLM:
    def generate_stream(self, messages: List[Dict[str, str]]) -> Generator[str, None, None]:
        raise NotImplementedError
