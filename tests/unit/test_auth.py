"""Unit tests for authentication module."""

import pytest
from euroleague.auth import OAuth2PKCEAuth, TokenInfo, InMemoryTokenStorage


class TestOAuth2PKCEAuth:
    """Test OAuth2 PKCE authentication."""

    def test_generate_authorization_url(self):
        """Test authorization URL generation."""
        auth = OAuth2PKCEAuth(client_id="test_client")
        url, state, verifier = auth.generate_authorization_url()

        assert "code_challenge=" in url
        assert "code_challenge_method=S256" in url
        assert "client_id=test_client" in url
        assert "state=" in url
        assert len(verifier) > 40
        assert len(state) > 20

    def test_generate_authorization_url_with_custom_state(self):
        """Test authorization URL with custom state."""
        auth = OAuth2PKCEAuth(client_id="test_client")
        url, state, verifier = auth.generate_authorization_url(state="custom_state")

        assert state == "custom_state"
        assert "state=custom_state" in url

    def test_code_challenge_is_valid(self):
        """Test S256 code challenge format."""
        auth = OAuth2PKCEAuth(client_id="test_client")
        challenge = auth._create_code_challenge("test_verifier")

        # S256 should produce base64url-encoded SHA256 (43 chars without padding)
        assert len(challenge) == 43
        assert "=" not in challenge  # No padding
        assert "+" not in challenge  # URL-safe
        assert "/" not in challenge  # URL-safe


class TestTokenInfo:
    """Test TokenInfo class."""

    def test_token_not_expired(self):
        """Test token expiry check."""
        token = TokenInfo(
            access_token="test",
            token_type="Bearer",
            expires_in=3600
        )
        assert not token.is_expired

    def test_token_serialization(self):
        """Test token to/from dict."""
        token = TokenInfo(
            access_token="test",
            token_type="Bearer",
            expires_in=3600,
            refresh_token="refresh"
        )
        data = token.to_dict()
        restored = TokenInfo.from_dict(data)

        assert restored.access_token == token.access_token
        assert restored.refresh_token == token.refresh_token


class TestInMemoryTokenStorage:
    """Test in-memory token storage."""

    def test_store_and_get(self):
        """Test storing and retrieving token."""
        storage = InMemoryTokenStorage()
        token = TokenInfo(
            access_token="test",
            token_type="Bearer",
            expires_in=3600
        )

        storage.store_token(token)
        retrieved = storage.get_token()

        assert retrieved is not None
        assert retrieved.access_token == "test"

    def test_clear(self):
        """Test clearing token."""
        storage = InMemoryTokenStorage()
        token = TokenInfo(
            access_token="test",
            token_type="Bearer",
            expires_in=3600
        )

        storage.store_token(token)
        storage.clear_token()

        assert storage.get_token() is None
