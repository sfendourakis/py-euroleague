"""Main client classes for the Euroleague API."""

from typing import Optional

from euroleague.api.v1 import V1API
from euroleague.api.v2 import V2API
from euroleague.api.v3 import V3API
from euroleague.auth import FileTokenStorage, OAuth2PKCEAuth, TokenInfo, TokenStorage
from euroleague.http import AsyncHTTPClient, HTTPClient
from euroleague.utils.constants import BASE_URL


class EuroleagueClient:
    """
    Main client for the Euroleague Basketball API (synchronous).

    Provides access to all API versions (v1, v2, v3) through a unified interface.

    Example:
        >>> client = EuroleagueClient(client_id="your_client_id")
        >>> # Authenticate
        >>> auth_url, state, verifier = client.get_authorization_url()
        >>> # After user authorizes, exchange code
        >>> client.authenticate(code="auth_code", code_verifier=verifier)
        >>> # Use the API
        >>> games = client.v2.games.list(competition_code="E", season_code="2024")

    For a pre-obtained token:
        >>> client = EuroleagueClient(client_id="your_client_id")
        >>> client.set_token(TokenInfo(access_token="...", token_type="Bearer", expires_in=3600))
        >>> # Now use the API directly
        >>> clubs = client.v2.clubs.list()
    """

    def __init__(
        self,
        client_id: str,
        redirect_uri: str = "http://localhost:8080/callback",
        token_storage: Optional[TokenStorage] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        base_url: str = BASE_URL,
    ) -> None:
        """
        Initialize the Euroleague API client.

        Args:
            client_id: OAuth2 client ID for authentication
            redirect_uri: OAuth2 redirect URI (default: localhost)
            token_storage: Optional custom token storage implementation.
                          Defaults to FileTokenStorage for persistence.
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            base_url: API base URL (for testing purposes)
        """
        if token_storage is None:
            token_storage = FileTokenStorage()

        self._auth = OAuth2PKCEAuth(
            client_id=client_id,
            redirect_uri=redirect_uri,
            token_storage=token_storage,
        )
        self._http = HTTPClient(
            auth=self._auth,
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

    def get_authorization_url(self, state: Optional[str] = None) -> tuple[str, str, str]:
        """
        Generate OAuth2 authorization URL for user authentication.

        The user should visit this URL in a browser to authorize the application.
        After authorization, they will be redirected to the redirect_uri with
        an authorization code.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Tuple of (authorization_url, state, code_verifier)
            Save the code_verifier to use when exchanging the authorization code.
        """
        return self._auth.generate_authorization_url(state)

    def authenticate(self, code: str, code_verifier: str) -> TokenInfo:
        """
        Complete authentication by exchanging authorization code for token.

        Args:
            code: Authorization code from OAuth callback
            code_verifier: PKCE code verifier from get_authorization_url()

        Returns:
            TokenInfo with the access token
        """
        return self._auth.exchange_code(code, code_verifier)

    def refresh_token(self) -> TokenInfo:
        """
        Refresh an expired access token.

        Returns:
            TokenInfo with the new access token

        Raises:
            AuthenticationError: If no refresh token is available
        """
        return self._auth.refresh_token()

    def set_token(self, token: TokenInfo) -> None:
        """
        Manually set a token (useful for pre-obtained tokens or testing).

        Args:
            token: TokenInfo to use for authentication
        """
        self._auth.set_token(token)

    def clear_token(self) -> None:
        """Clear the stored authentication token."""
        self._auth.clear_token()

    def close(self) -> None:
        """Close the HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> "EuroleagueClient":
        """Enter context manager."""
        return self

    def __exit__(self, *args) -> None:
        """Exit context manager and close client."""
        self.close()


class AsyncEuroleagueClient:
    """
    Async client for the Euroleague Basketball API.

    Provides access to all API versions (v1, v2, v3) through a unified interface
    using async/await patterns.

    Example:
        >>> async with AsyncEuroleagueClient(client_id="your_client_id") as client:
        ...     # Set token (async auth flow would happen elsewhere)
        ...     client.set_token(TokenInfo(...))
        ...     # Use the API with async methods
        ...     clubs = await client.v2.clubs.list_async()
        ...     games = await client.v2.games.list_async(
        ...         competition_code="E", season_code="2024"
        ...     )

    Parallel requests:
        >>> async with AsyncEuroleagueClient(client_id="...") as client:
        ...     import asyncio
        ...     games, standings, leaders = await asyncio.gather(
        ...         client.v2.games.list_async("E", "2024"),
        ...         client.v3.standings.basic_async("E", "2024", 10),
        ...         client.v3.player_stats.leaders_async("E")
        ...     )
    """

    def __init__(
        self,
        client_id: str,
        redirect_uri: str = "http://localhost:8080/callback",
        token_storage: Optional[TokenStorage] = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        base_url: str = BASE_URL,
    ) -> None:
        """
        Initialize the async Euroleague API client.

        Args:
            client_id: OAuth2 client ID for authentication
            redirect_uri: OAuth2 redirect URI (default: localhost)
            token_storage: Optional custom token storage implementation.
                          Defaults to FileTokenStorage for persistence.
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            base_url: API base URL (for testing purposes)
        """
        if token_storage is None:
            token_storage = FileTokenStorage()

        self._auth = OAuth2PKCEAuth(
            client_id=client_id,
            redirect_uri=redirect_uri,
            token_storage=token_storage,
        )
        self._http = AsyncHTTPClient(
            auth=self._auth,
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

    def get_authorization_url(self, state: Optional[str] = None) -> tuple[str, str, str]:
        """
        Generate OAuth2 authorization URL for user authentication.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Tuple of (authorization_url, state, code_verifier)
        """
        return self._auth.generate_authorization_url(state)

    async def authenticate(self, code: str, code_verifier: str) -> TokenInfo:
        """
        Complete authentication by exchanging authorization code for token.

        Args:
            code: Authorization code from OAuth callback
            code_verifier: PKCE code verifier from get_authorization_url()

        Returns:
            TokenInfo with the access token
        """
        return await self._auth.exchange_code_async(code, code_verifier)

    async def refresh_token(self) -> TokenInfo:
        """
        Refresh an expired access token.

        Returns:
            TokenInfo with the new access token

        Raises:
            AuthenticationError: If no refresh token is available
        """
        return await self._auth.refresh_token_async()

    def set_token(self, token: TokenInfo) -> None:
        """
        Manually set a token (useful for pre-obtained tokens or testing).

        Args:
            token: TokenInfo to use for authentication
        """
        self._auth.set_token(token)

    def clear_token(self) -> None:
        """Clear the stored authentication token."""
        self._auth.clear_token()

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        await self._http.close()

    async def __aenter__(self) -> "AsyncEuroleagueClient":
        """Enter async context manager."""
        return self

    async def __aexit__(self, *args) -> None:
        """Exit async context manager and close client."""
        await self.close()
