"""LLM service — abstract wrapper around LLM API calls.

Supports OpenAI-compatible APIs. Falls back to stub responses when
no API key is configured.

Environment variables (in order of precedence):
  LLM_API_KEY       — API key for the LLM provider
  LLM_BASE_URL      — base URL (default: https://api.openai.com/v1)
  LLM_MODEL         — model name (default: gpt-4o-mini)
"""

from __future__ import annotations

import os
from typing import Any

import httpx

from config.settings import settings

_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY") or getattr(settings, "LLM_API_KEY", None) or getattr(settings, "OPENAI_API_KEY", None)
_BASE_URL = os.getenv("LLM_BASE_URL") or "https://api.openai.com/v1"
_MODEL_NAME = os.getenv("LLM_MODEL") or "gpt-4o-mini"


async def call_llm(messages: list[dict[str, str]], **kwargs: Any) -> str:
    """Call the configured LLM and return the assistant reply text.

    Parameters
    ----------
    messages :
        List of ``{"role": "system"|"user"|"assistant", "content": "..."}`` dicts.
    **kwargs :
        Extra parameters forwarded to the LLM (temperature, max_tokens, etc.).

    Returns
    -------
        The assistant's reply text.
    """
    if not _API_KEY:
        return _stub_response(messages)

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": _MODEL_NAME,
                "messages": messages,
                **kwargs,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


def _stub_response(messages: list[dict[str, str]]) -> str:
    """Stub response when no LLM API key is configured."""
    last_user = ""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user = msg.get("content", "")
            break

    if not last_user:
        return "Hello! I'm a stub agent. Connect an LLM API key for real responses."

    # Simple heuristic stub replies
    greetings = ("hi", "hello", "hey", "hola", "你好")
    if last_user.lower().startswith(greetings):
        return f"That's a great greeting! I'm happy to chat about this topic."

    return f"I hear you say \"{last_user[:50]}\". That's interesting — tell me more!"
