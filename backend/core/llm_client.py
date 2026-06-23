"""轻量级 LLM API 客户端——OpenAI 兼容格式。"""

from __future__ import annotations

import json
from typing import Any, Protocol

import httpx

from config.llm import llm_settings


class LLMClient(Protocol):
    async def chat(self, *, system: str, messages: list[dict], **kwargs: Any) -> str: ...


class OpenAICompatibleClient:
    """面向 OpenAI 兼容 API 的 HTTP 客户端（Anthropic / 本地 Ollama 等均可复用）。"""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
    ) -> None:
        self.base_url = (base_url or llm_settings.LLM_BASE_URL).rstrip("/")
        self.api_key = api_key or llm_settings.LLM_API_KEY
        self.model = model or llm_settings.LLM_MODEL
        # 判断是否为 Anthropic 风格（header 不同）
        self._anthropic = "anthropic" in (self.base_url or "").lower() or "anthropic" in llm_settings.LLM_PROVIDER.lower()

    # ---- public ----

    async def chat(self, *, system: str, messages: list[dict], **kwargs: Any) -> str:
        """调用聊天接口，返回文本内容。"""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": self._build_messages(system, messages),
            "temperature": kwargs.get("temperature", llm_settings.LLM_TEMPERATURE),
            "max_tokens": kwargs.get("max_tokens", llm_settings.LLM_MAX_TOKENS),
        }

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        if self._anthropic:
            headers["anthropic-version"] = "2023-06-01"

        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{self.base_url}/v1/chat/completions" if not self._anthropic else f"{self.base_url}/v1/messages",
                headers=headers,
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        return self._extract_text(data)

    # ---- internals ----

    def _build_messages(self, system: str, history: list[dict]) -> list[dict]:
        msgs: list[dict] = [{"role": "system", "content": system}]
        msgs.extend(history)
        return msgs

    def _extract_text(self, data: dict) -> str:
        if self._anthropic:
            # Anthropic response format
            for block in data.get("content", []):
                if block.get("type") == "text":
                    return block["text"]
            return ""
        # OpenAI-compatible format
        return data["choices"][0]["message"]["content"]


# ---- 单例 ----

_llm_client: OpenAICompatibleClient | None = None


def get_llm_client() -> OpenAICompatibleClient:
    global _llm_client
    if _llm_client is None:
        _llm_client = OpenAICompatibleClient()
    return _llm_client
