"""Unit tests for client module."""

import pytest
from euroleague import EuroleagueClient, AsyncEuroleagueClient
from euroleague.auth import InMemoryTokenStorage


class TestEuroleagueClient:
    """Test synchronous client."""

    def test_initialization(self):
        """Test client initialization."""
        client = EuroleagueClient(
            client_id="test_client",
            token_storage=InMemoryTokenStorage()
        )
        assert client.v1 is not None
        assert client.v2 is not None
        assert client.v3 is not None

    def test_context_manager(self):
        """Test client as context manager."""
        with EuroleagueClient(
            client_id="test_client",
            token_storage=InMemoryTokenStorage()
        ) as client:
            assert client is not None

    def test_authorization_url(self):
        """Test authorization URL generation."""
        client = EuroleagueClient(
            client_id="test_client",
            token_storage=InMemoryTokenStorage()
        )
        url, state, verifier = client.get_authorization_url()

        assert "test_client" in url
        assert len(state) > 0
        assert len(verifier) > 0


class TestAsyncEuroleagueClient:
    """Test asynchronous client."""

    def test_initialization(self):
        """Test async client initialization."""
        client = AsyncEuroleagueClient(
            client_id="test_client",
            token_storage=InMemoryTokenStorage()
        )
        assert client.v1 is not None
        assert client.v2 is not None
        assert client.v3 is not None

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async client as context manager."""
        async with AsyncEuroleagueClient(
            client_id="test_client",
            token_storage=InMemoryTokenStorage()
        ) as client:
            assert client is not None
