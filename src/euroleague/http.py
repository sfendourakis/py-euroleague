"""HTTP client layer for the Euroleague API."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

import httpx

from euroleague.exceptions import NetworkError, TimeoutError, raise_for_status
from euroleague.utils.constants import BASE_URL

if TYPE_CHECKING:
    from euroleague.auth import OAuth2PKCEAuth


class HTTPClient:
    """Synchronous HTTP client with retry logic and authentication."""

    def __init__(
        self,
        auth: OAuth2PKCEAuth,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            auth: OAuth2 PKCE authentication handler
            base_url: API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self._base_url = base_url.rstrip("/")
        self._auth = auth
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
        )

    def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make authenticated GET request.

        Args:
            path: API endpoint path
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            TimeoutError: If request times out after all retries
            NetworkError: If network error occurs after all retries
            Various API exceptions based on status code
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = self._auth.get_auth_header()

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                response = self._client.get(url, params=params, headers=headers)
                body = response.json() if response.content else {}
                raise_for_status(
                    response.status_code,
                    body,
                    dict(response.headers),
                )
                return body
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt == self._max_retries - 1:
                    raise TimeoutError(f"Request timed out after {self._timeout}s") from e
            except httpx.NetworkError as e:
                last_exception = e
                if attempt == self._max_retries - 1:
                    raise NetworkError(str(e)) from e

        # This should not be reached, but just in case
        raise NetworkError(f"Request failed after {self._max_retries} retries") from last_exception

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._client.close()


class AsyncHTTPClient:
    """Asynchronous HTTP client with retry logic and authentication."""

    def __init__(
        self,
        auth: OAuth2PKCEAuth,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the async HTTP client.

        Args:
            auth: OAuth2 PKCE authentication handler
            base_url: API base URL
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self._base_url = base_url.rstrip("/")
        self._auth = auth
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        )

    async def get(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make authenticated GET request.

        Args:
            path: API endpoint path
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            TimeoutError: If request times out after all retries
            NetworkError: If network error occurs after all retries
            Various API exceptions based on status code
        """
        url = f"{self._base_url}/{path.lstrip('/')}"
        headers = self._auth.get_auth_header()

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                response = await self._client.get(url, params=params, headers=headers)
                body = response.json() if response.content else {}
                raise_for_status(
                    response.status_code,
                    body,
                    dict(response.headers),
                )
                return body
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt == self._max_retries - 1:
                    raise TimeoutError(f"Request timed out after {self._timeout}s") from e
            except httpx.NetworkError as e:
                last_exception = e
                if attempt == self._max_retries - 1:
                    raise NetworkError(str(e)) from e

        # This should not be reached, but just in case
        raise NetworkError(f"Request failed after {self._max_retries} retries") from last_exception

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._client.aclose()
