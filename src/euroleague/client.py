"""Main client classes for the Euroleague API."""

from typing import Any

from euroleague.api.v1 import V1API
from euroleague.api.v2 import V2API
from euroleague.api.v3 import V3API
from euroleague.http import AsyncHTTPClient, HTTPClient
from euroleague.utils.constants import BASE_URL


class EuroleagueClient:
    """
    Main client for the Euroleague Basketball API (synchronous).

    Provides access to all API versions (v1, v2, v3) through a unified interface.

    Example:
        >>> with EuroleagueClient() as client:
        ...     games = client.v2.games.list(competition_code="E", season_code="2024")
        ...     clubs = client.v2.clubs.list()
    """

    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
        base_url: str = BASE_URL,
    ) -> None:
        """
        Initialize the Euroleague API client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            base_url: API base URL (for testing purposes)
        """
        self._http = HTTPClient(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize API version namespaces
        self._v1 = V1API(self._http)
        self._v2 = V2API(self._http)
        self._v3 = V3API(self._http)

    @property
    def v1(self) -> V1API:
        """Access V1 API endpoints (legacy/simple)."""
        return self._v1

    @property
    def v2(self) -> V2API:
        """Access V2 API endpoints (comprehensive)."""
        return self._v2

    @property
    def v3(self) -> V3API:
        """Access V3 API endpoints (statistics-focused)."""
        return self._v3

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> "EuroleagueClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context manager and close client."""
        self.close()


class AsyncEuroleagueClient:
    """
    Async client for the Euroleague Basketball API.

    Provides access to all API versions (v1, v2, v3) through a unified interface
    using async/await patterns.

    Example:
        >>> async with AsyncEuroleagueClient() as client:
        ...     clubs = await client.v2.clubs.list_async()
        ...     games = await client.v2.games.list_async(
        ...         competition_code="E", season_code="2024"
        ...     )

    Parallel requests:
        >>> async with AsyncEuroleagueClient() as client:
        ...     import asyncio
        ...     games, standings, leaders = await asyncio.gather(
        ...         client.v2.games.list_async("E", "2024"),
        ...         client.v3.standings.basic_async("E", "2024", 10),
        ...         client.v3.player_stats.leaders_async("E")
        ...     )
    """

    def __init__(
        self,
        timeout: float = 30.0,
        max_retries: int = 3,
        base_url: str = BASE_URL,
    ) -> None:
        """
        Initialize the async Euroleague API client.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            base_url: API base URL (for testing purposes)
        """
        self._http = AsyncHTTPClient(
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize API version namespaces
        self._v1 = V1API(self._http)
        self._v2 = V2API(self._http)
        self._v3 = V3API(self._http)

    @property
    def v1(self) -> V1API:
        """Access V1 API endpoints (legacy/simple)."""
        return self._v1

    @property
    def v2(self) -> V2API:
        """Access V2 API endpoints (comprehensive)."""
        return self._v2

    @property
    def v3(self) -> V3API:
        """Access V3 API endpoints (statistics-focused)."""
        return self._v3

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncEuroleagueClient":
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Exit async context manager and close client."""
        await self.close()
