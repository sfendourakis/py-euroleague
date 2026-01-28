"""Unit tests for client module."""

import pytest

from euroleague import AsyncEuroleagueClient, EuroleagueClient


class TestEuroleagueClient:
    """Test synchronous client."""

    def test_initialization(self):
        """Test client initialization."""
        client = EuroleagueClient()
        assert client.v1 is not None
        assert client.v2 is not None
        assert client.v3 is not None

    def test_context_manager(self):
        """Test client as context manager."""
        with EuroleagueClient() as client:
            assert client is not None


class TestAsyncEuroleagueClient:
    """Test asynchronous client."""

    def test_initialization(self):
        """Test async client initialization."""
        client = AsyncEuroleagueClient()
        assert client.v1 is not None
        assert client.v2 is not None
        assert client.v3 is not None

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async client as context manager."""
        async with AsyncEuroleagueClient() as client:
            assert client is not None
