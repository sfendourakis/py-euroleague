"""HTTP client layer for the Euroleague API."""

from __future__ import annotations

import asyncio
import json
import logging
import time
from typing import Any

import httpx

from euroleague._version import __version__
from euroleague.exceptions import APIError, NetworkError, TimeoutError, raise_for_status
from euroleague.utils.constants import BASE_URL

logger = logging.getLogger(__name__)

# Default headers for all requests
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": f"py-euroleague/{__version__}",
}


def _calculate_backoff(attempt: int, base_delay: float = 0.5, max_delay: float = 30.0) -> float:
    """Calculate exponential backoff delay.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay in seconds

    Returns:
        Delay in seconds for current attempt
    """
    delay: float = base_delay * (2 ** attempt)
    return min(delay, max_delay)


class HTTPClient:
    """Synchronous HTTP client with retry logic and exponential backoff."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the HTTP client.

        Args:
            base_url: API base URL (must use HTTPS)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests

        Raises:
            ValueError: If base_url does not use HTTPS
        """
        if not base_url.startswith("https://"):
            raise ValueError("base_url must use HTTPS for security")

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.Client(
            timeout=timeout,
            follow_redirects=True,
            verify=True,
            headers=DEFAULT_HEADERS,
        )
        logger.debug(f"Initialized HTTPClient with base_url={self._base_url}")

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make GET request with automatic retries and exponential backoff.

        Args:
            path: API endpoint path
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            TimeoutError: If request times out after all retries
            NetworkError: If network error occurs after all retries
            APIError: If API returns an error response
            NotFoundError: If resource is not found (404)
            RateLimitError: If rate limit is exceeded (429)
            ValidationError: If request validation fails (400)
        """
        url = f"{self._base_url}/{path.lstrip('/')}"

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exception: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                logger.debug(f"GET {url} (attempt {attempt + 1}/{self._max_retries})")
                response = self._client.get(url, params=params)
                try:
                    body = response.json() if response.content else {}
                except json.JSONDecodeError as e:
                    raise APIError(
                        f"Invalid JSON response: {response.text[:200]}",
                        response.status_code,
                    ) from e
                raise_for_status(
                    response.status_code,
                    body,
                    dict(response.headers),
                )
                logger.debug(f"GET {url} completed successfully")
                return body
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    delay = _calculate_backoff(attempt)
                    logger.warning(
                        f"Request to {url} timed out, retrying in {delay:.1f}s "
                        f"(attempt {attempt + 1}/{self._max_retries})"
                    )
                    time.sleep(delay)
                else:
                    logger.error(
                        f"Request to {url} timed out after {self._max_retries} attempts"
                    )
                    raise TimeoutError(f"Request timed out after {self._timeout}s") from e
            except httpx.NetworkError as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    delay = _calculate_backoff(attempt)
                    logger.warning(
                        f"Network error for {url}, retrying in {delay:.1f}s "
                        f"(attempt {attempt + 1}/{self._max_retries}): {e}"
                    )
                    time.sleep(delay)
                else:
                    logger.error(
                        f"Network error for {url} after {self._max_retries} attempts: {e}"
                    )
                    raise NetworkError(str(e)) from e

        # This should not be reached, but just in case
        raise NetworkError(f"Request failed after {self._max_retries} retries") from last_exception

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        logger.debug("Closing HTTPClient")
        self._client.close()


class AsyncHTTPClient:
    """Asynchronous HTTP client with retry logic and exponential backoff."""

    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
    ) -> None:
        """Initialize the async HTTP client.

        Args:
            base_url: API base URL (must use HTTPS)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests

        Raises:
            ValueError: If base_url does not use HTTPS
        """
        if not base_url.startswith("https://"):
            raise ValueError("base_url must use HTTPS for security")

        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            verify=True,
            headers=DEFAULT_HEADERS,
        )
        logger.debug(f"Initialized AsyncHTTPClient with base_url={self._base_url}")

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make GET request with automatic retries and exponential backoff.

        Args:
            path: API endpoint path
            params: Optional query parameters

        Returns:
            Parsed JSON response

        Raises:
            TimeoutError: If request times out after all retries
            NetworkError: If network error occurs after all retries
            APIError: If API returns an error response
            NotFoundError: If resource is not found (404)
            RateLimitError: If rate limit is exceeded (429)
            ValidationError: If request validation fails (400)
        """
        url = f"{self._base_url}/{path.lstrip('/')}"

        # Filter out None values from params
        if params:
            params = {k: v for k, v in params.items() if v is not None}

        last_exception: Exception | None = None

        for attempt in range(self._max_retries):
            try:
                logger.debug(f"GET {url} (attempt {attempt + 1}/{self._max_retries})")
                response = await self._client.get(url, params=params)
                try:
                    body = response.json() if response.content else {}
                except json.JSONDecodeError as e:
                    raise APIError(
                        f"Invalid JSON response: {response.text[:200]}",
                        response.status_code,
                    ) from e
                raise_for_status(
                    response.status_code,
                    body,
                    dict(response.headers),
                )
                logger.debug(f"GET {url} completed successfully")
                return body
            except httpx.TimeoutException as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    delay = _calculate_backoff(attempt)
                    logger.warning(
                        f"Request to {url} timed out, retrying in {delay:.1f}s "
                        f"(attempt {attempt + 1}/{self._max_retries})"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"Request to {url} timed out after {self._max_retries} attempts"
                    )
                    raise TimeoutError(f"Request timed out after {self._timeout}s") from e
            except httpx.NetworkError as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    delay = _calculate_backoff(attempt)
                    logger.warning(
                        f"Network error for {url}, retrying in {delay:.1f}s "
                        f"(attempt {attempt + 1}/{self._max_retries}): {e}"
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"Network error for {url} after {self._max_retries} attempts: {e}"
                    )
                    raise NetworkError(str(e)) from e

        # This should not be reached, but just in case
        raise NetworkError(f"Request failed after {self._max_retries} retries") from last_exception

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        logger.debug("Closing AsyncHTTPClient")
        await self._client.aclose()
