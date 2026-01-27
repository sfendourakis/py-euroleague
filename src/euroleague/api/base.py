"""Base API class for all endpoint groups."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Union

if TYPE_CHECKING:
    from euroleague.http import AsyncHTTPClient, HTTPClient


class BaseAPI:
    """Base class for all API endpoint groups.

    Provides common functionality for building URLs and making requests.
    """

    def __init__(
        self,
        http_client: Union[HTTPClient, AsyncHTTPClient],
        base_path: str = "",
    ) -> None:
        """Initialize the API endpoint group.

        Args:
            http_client: HTTP client for making requests
            base_path: Base path for this API group (e.g., '/v1/games')
        """
        self._http = http_client
        self._base_path = base_path.strip("/")

    def _build_path(self, *parts: str) -> str:
        """Construct URL path from parts.

        Args:
            *parts: Path segments to join

        Returns:
            Complete path string
        """
        clean_parts = [str(p).strip("/") for p in parts if p]
        if self._base_path:
            return "/".join([self._base_path, *clean_parts])
        return "/".join(clean_parts)

    def _get(
        self,
        *path_parts: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make GET request (synchronous).

        Args:
            *path_parts: Path segments to append to base path
            params: Optional query parameters

        Returns:
            Parsed JSON response
        """
        path = self._build_path(*path_parts)
        return self._http.get(path, params=params)

    async def _get_async(
        self,
        *path_parts: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make GET request (asynchronous).

        Args:
            *path_parts: Path segments to append to base path
            params: Optional query parameters

        Returns:
            Parsed JSON response
        """
        path = self._build_path(*path_parts)
        return await self._http.get(path, params=params)
