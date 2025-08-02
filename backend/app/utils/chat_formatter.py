# backend/app/core/utils/chat_formatter.py
from typing import List, Dict

from backend.app.models.chat import ChatMessage

DEFAULT_SYSTEM_PROMPT = "You are a professional assistant helping with enterprise-grade tasks. Be concise, formal, and knowledgeable."


def format_chat_with_roles(messages: List[ChatMessage]) -> str:
    formatted = ""
    for msg in messages:
        role = msg.role
        content = msg.content
        if role == "system":
            formatted += f"<|system|>\n{content}\n"
        elif role == "user":
            formatted += f"<|user|>\n{content}\n"
        elif role == "assistant":
            formatted += f"<|assistant|>\n{content}\n"
    formatted += "<|assistant|>\n"
    return formatted

def format_chat_with_roles_old(messages: List[Dict[str, str]], system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> str:
    """Converts list of role-based messages into llama-cpp prompt format"""
    print(messages)
    all_messages = [{"role": "system", "content": system_prompt}] + messages
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
    formatted += "<|assistant|>\n"
    return formatted

