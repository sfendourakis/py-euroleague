"""
py-euroleague - Python wrapper for the Euroleague Basketball API.

This library provides a clean, Pythonic interface to access the Euroleague API,
supporting all three API versions (v1, v2, v3) with both synchronous and
asynchronous clients.

Example:
    >>> from euroleague import EuroleagueClient
    >>> client = EuroleagueClient(client_id="your_client_id")
    >>> clubs = client.v2.clubs.list()
"""

from euroleague._version import __version__
from euroleague.client import AsyncEuroleagueClient, EuroleagueClient
from euroleague.exceptions import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    EuroleagueError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "EuroleagueClient",
    "AsyncEuroleagueClient",
    # Exceptions
    "EuroleagueError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "RateLimitError",
    "ValidationError",
    "APIError",
    "NetworkError",
    "TimeoutError",
]
