"""Tests for utils/security.py — password hashing and JWT."""

from datetime import timedelta

from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


class TestHashPassword:
    def test_hash_returns_bytes(self):
        hashed = hash_password("secret123")
        assert isinstance(hashed, bytes)

    def test_different_hashes_per_call(self):
        h1 = hash_password("same_password")
        h2 = hash_password("same_password")
        assert h1 != h2  # bcrypt salts differ

    def test_hash_does_not_crash_long_password(self):
        long_pw = "a" * 70
        hashed = hash_password(long_pw)
        assert isinstance(hashed, bytes)


class TestVerifyPassword:
    def test_correct_password(self):
        pw = "my_secret"
        hashed = hash_password(pw)
        assert verify_password(pw, hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("correct_password")
        assert verify_password("wrong_password", hashed) is False

    def test_empty_password(self):
        hashed = hash_password("")
        assert verify_password("", hashed) is True
        assert verify_password("x", hashed) is False


class TestCreateAccessToken:
    def test_returns_string(self):
        token = create_access_token({"sub": "123", "email": "test@example.com"})
        assert isinstance(token, str)

    def test_contains_three_parts(self):
        token = create_access_token({"sub": "123"})
        parts = token.split(".")
        assert len(parts) == 3

    def test_custom_expires_delta(self):
        token = create_access_token({"sub": "123"}, expires_delta=timedelta(minutes=5))
        assert isinstance(token, str)

    def test_different_data_different_token(self):
        t1 = create_access_token({"sub": "user1"})
        t2 = create_access_token({"sub": "user2"})
        assert t1 != t2


class TestDecodeAccessToken:
    def test_decode_valid_token(self):
        token = create_access_token({"sub": "abc-123", "email": "test@example.com"})
        payload = decode_access_token(token)
        assert payload is not None
        assert payload["sub"] == "abc-123"
        assert payload["email"] == "test@example.com"

    def test_decode_invalid_token(self):
        assert decode_access_token("not.a.token") is None

    def test_decode_random_string(self):
        assert decode_access_token("xyz-random-gibberish") is None

    def test_decode_empty_string(self):
        assert decode_access_token("") is None
