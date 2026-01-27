"""Pytest configuration and fixtures."""

import pytest
from unittest.mock import Mock, AsyncMock

from euroleague import EuroleagueClient, AsyncEuroleagueClient
from euroleague.auth import TokenInfo, InMemoryTokenStorage


@pytest.fixture
def token_storage():
    """Provide pre-authenticated token storage."""
    storage = InMemoryTokenStorage()
    storage.store_token(TokenInfo(
        access_token="test_token",
        token_type="Bearer",
        expires_in=3600
    ))
    return storage


@pytest.fixture
def mock_http_client():
    """Mock HTTP client for unit tests."""
    mock = Mock()
    mock.get = Mock(return_value={})
    return mock


@pytest.fixture
def mock_async_http_client():
    """Mock async HTTP client for unit tests."""
    mock = AsyncMock()
    mock.get = AsyncMock(return_value={})
    return mock


@pytest.fixture
def client(token_storage):
    """Provide configured test client."""
    return EuroleagueClient(
        client_id="test_client",
        token_storage=token_storage
    )


@pytest.fixture
def async_client(token_storage):
    """Provide async test client."""
    return AsyncEuroleagueClient(
        client_id="test_client",
        token_storage=token_storage
    )
