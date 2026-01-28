"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock, Mock

import pytest

from euroleague import AsyncEuroleagueClient, EuroleagueClient


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
def client():
    """Provide configured test client."""
    return EuroleagueClient()


@pytest.fixture
def async_client():
    """Provide async test client."""
    return AsyncEuroleagueClient()
