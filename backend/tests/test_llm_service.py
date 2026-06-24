"""Tests for LLM service stub response."""

from services.llm_service import _stub_response


class TestStubResponse:
    def test_no_user_message(self):
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "assistant", "content": "Hi there!"},
        ]
        result = _stub_response(messages)
        assert "stub agent" in result.lower() or "connect" in result.lower()

    def test_greeting_hello(self):
        messages = [{"role": "user", "content": "hello"}]
        result = _stub_response(messages)
        assert "great" in result.lower() or "happy" in result.lower()

    def test_greeting_hi(self):
        messages = [{"role": "user", "content": "hi"}]
        result = _stub_response(messages)
        assert "great" in result.lower() or "happy" in result.lower()

    def test_greeting_hey(self):
        messages = [{"role": "user", "content": "hey"}]
        result = _stub_response(messages)
        assert "great" in result.lower() or "happy" in result.lower()

    def test_non_greeting(self):
        messages = [{"role": "user", "content": "Tell me about quantum physics"}]
        result = _stub_response(messages)
        assert "interesting" in result.lower() or "tell me more" in result.lower()

    def test_last_user_message_in_history(self):
        messages = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "response"},
            {"role": "user", "content": "second question"},
        ]
        result = _stub_response(messages)
        assert "second question" in result

    def test_truncates_long_content(self):
        long_msg = "x" * 200
        messages = [{"role": "user", "content": long_msg}]
        result = _stub_response(messages)
        # Should not crash
        assert isinstance(result, str)
