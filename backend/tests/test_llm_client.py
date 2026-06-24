"""Tests for LLM client message building and response extraction."""

import pytest

from core.llm_client import OpenAICompatibleClient


class TestBuildMessages:
    def test_includes_system_message(self):
        client = OpenAICompatibleClient(api_key="test", base_url="https://test.com")
        msgs = client._build_messages("You are helpful.", [])
        assert len(msgs) == 1
        assert msgs[0] == {"role": "system", "content": "You are helpful."}

    def test_appends_history(self):
        client = OpenAICompatibleClient(api_key="test", base_url="https://test.com")
        history = [{"role": "user", "content": "hello"}]
        msgs = client._build_messages("sys", history)
        assert len(msgs) == 2
        assert msgs[1] == {"role": "user", "content": "hello"}

    def test_full_conversation(self):
        client = OpenAICompatibleClient(api_key="test", base_url="https://test.com")
        history = [
            {"role": "user", "content": "hi"},
            {"role": "assistant", "content": "hello!"},
        ]
        msgs = client._build_messages("be nice", history)
        assert len(msgs) == 3
        assert msgs[0]["role"] == "system"
        assert msgs[1]["role"] == "user"
        assert msgs[2]["role"] == "assistant"


class TestExtractText:
    def test_openai_format(self):
        client = OpenAICompatibleClient(api_key="test", base_url="https://test.com")
        data = {
            "choices": [{"message": {"content": "This is the answer"}}],
        }
        assert client._extract_text(data) == "This is the answer"

    def test_anthropic_text_block(self):
        client = OpenAICompatibleClient(
            api_key="test", base_url="https://api.anthropic.com"
        )
        data = {
            "content": [
                {"type": "text", "text": "Anthropic reply"},
                {"type": "tool_use", "id": "123"},
            ],
        }
        assert client._extract_text(data) == "Anthropic reply"

    def test_anthropic_empty_content(self):
        client = OpenAICompatibleClient(
            api_key="test", base_url="https://api.anthropic.com"
        )
        data = {"content": []}
        assert client._extract_text(data) == ""

    def test_anthropic_no_text_block(self):
        client = OpenAICompatibleClient(
            api_key="test", base_url="https://api.anthropic.com"
        )
        data = {"content": [{"type": "tool_use", "id": "123"}]}
        assert client._extract_text(data) == ""

    def test_openai_missing_choice_raises(self):
        client = OpenAICompatibleClient(api_key="test", base_url="https://test.com")
        data = {"choices": []}
        # Depending on python version, this may raise IndexError or KeyError
        with pytest.raises(Exception):
            client._extract_text(data)
