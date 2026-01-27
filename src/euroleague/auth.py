"""OAuth2 PKCE authentication for the Euroleague API."""

from __future__ import annotations

import base64
import hashlib
import json
import secrets
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import urlencode

import httpx

from euroleague.exceptions import AuthenticationError
from euroleague.utils.constants import AUTH_URL, OAUTH_SCOPE, TOKEN_URL


@dataclass
class TokenInfo:
    """OAuth2 token information."""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    _obtained_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_expired(self) -> bool:
        """Check if token has expired (with 60s buffer)."""
        expiry = self._obtained_at + timedelta(seconds=self.expires_in - 60)
        return datetime.utcnow() >= expiry

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "_obtained_at": self._obtained_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> TokenInfo:
        """Create from dictionary."""
        obtained_at = data.get("_obtained_at")
        if obtained_at:
            obtained_at = datetime.fromisoformat(obtained_at)
        else:
            obtained_at = datetime.utcnow()

        return cls(
            access_token=data["access_token"],
            token_type=data["token_type"],
            expires_in=data["expires_in"],
            refresh_token=data.get("refresh_token"),
            scope=data.get("scope"),
            _obtained_at=obtained_at,
        )


class TokenStorage(ABC):
    """Abstract base for token persistence."""

    @abstractmethod
    def store_token(self, token: TokenInfo) -> None:
        """Store the token."""
        ...

    @abstractmethod
    def get_token(self) -> Optional[TokenInfo]:
        """Retrieve the stored token."""
        ...

    @abstractmethod
    def clear_token(self) -> None:
        """Clear the stored token."""
        ...


class InMemoryTokenStorage(TokenStorage):
    """Simple in-memory token storage."""

    def __init__(self) -> None:
        self._token: Optional[TokenInfo] = None

    def store_token(self, token: TokenInfo) -> None:
        """Store the token in memory."""
        self._token = token

    def get_token(self) -> Optional[TokenInfo]:
        """Retrieve the token from memory."""
        return self._token

    def clear_token(self) -> None:
        """Clear the token from memory."""
        self._token = None


class FileTokenStorage(TokenStorage):
    """File-based token storage for persistence across sessions."""

    def __init__(self, path: str = "~/.euroleague/token.json") -> None:
        """Initialize file-based storage.

        Args:
            path: Path to the token file (supports ~ expansion)
        """
        self._path = Path(path).expanduser()

    def store_token(self, token: TokenInfo) -> None:
        """Store the token to file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(token.to_dict(), f)

    def get_token(self) -> Optional[TokenInfo]:
        """Retrieve the token from file."""
        if not self._path.exists():
            return None
        try:
            with open(self._path) as f:
                data = json.load(f)
            return TokenInfo.from_dict(data)
        except (json.JSONDecodeError, KeyError):
            return None

    def clear_token(self) -> None:
        """Delete the token file."""
        if self._path.exists():
            self._path.unlink()


class OAuth2PKCEAuth:
    """
    OAuth2 PKCE authentication handler for Euroleague API.

    Implements the Authorization Code flow with PKCE (Proof Key for Code Exchange)
    for secure authentication without client secrets.
    """

    def __init__(
        self,
        client_id: str,
        redirect_uri: str = "http://localhost:8080/callback",
        token_storage: Optional[TokenStorage] = None,
    ) -> None:
        """Initialize the OAuth2 PKCE authentication handler.

        Args:
            client_id: OAuth2 client ID
            redirect_uri: OAuth2 redirect URI
            token_storage: Optional custom token storage implementation
        """
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self._token_storage = token_storage or InMemoryTokenStorage()
        self._code_verifier: Optional[str] = None

    def generate_authorization_url(self, state: Optional[str] = None) -> tuple[str, str, str]:
        """
        Generate authorization URL with PKCE challenge.

        Args:
            state: Optional state parameter for CSRF protection

        Returns:
            Tuple of (authorization_url, state, code_verifier)
        """
        self._code_verifier = secrets.token_urlsafe(64)
        code_challenge = self._create_code_challenge(self._code_verifier)
        state = state or secrets.token_urlsafe(32)

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": OAUTH_SCOPE,
            "state": state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }

        url = f"{AUTH_URL}?{urlencode(params)}"
        return url, state, self._code_verifier

    def exchange_code(self, code: str, code_verifier: str) -> TokenInfo:
        """
        Exchange authorization code for access token (synchronous).

        Args:
            code: Authorization code from OAuth callback
            code_verifier: PKCE code verifier from generate_authorization_url()

        Returns:
            TokenInfo with access token and metadata
        """
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
        }

        with httpx.Client() as client:
            response = client.post(TOKEN_URL, data=data)

        if response.status_code != 200:
            error = response.json() if response.content else {}
            raise AuthenticationError(
                f"Token exchange failed: {error.get('error_description', error.get('error', 'Unknown error'))}"
            )

        token_data = response.json()
        token = TokenInfo(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
        )
        self._token_storage.store_token(token)
        return token

    async def exchange_code_async(self, code: str, code_verifier: str) -> TokenInfo:
        """
        Exchange authorization code for access token (asynchronous).

        Args:
            code: Authorization code from OAuth callback
            code_verifier: PKCE code verifier from generate_authorization_url()

        Returns:
            TokenInfo with access token and metadata
        """
        data = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "code_verifier": code_verifier,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, data=data)

        if response.status_code != 200:
            error = response.json() if response.content else {}
            raise AuthenticationError(
                f"Token exchange failed: {error.get('error_description', error.get('error', 'Unknown error'))}"
            )

        token_data = response.json()
        token = TokenInfo(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
        )
        self._token_storage.store_token(token)
        return token

    def refresh_token(self) -> TokenInfo:
        """
        Refresh an expired access token (synchronous).

        Returns:
            New TokenInfo with refreshed access token

        Raises:
            AuthenticationError: If no refresh token is available
        """
        current_token = self._token_storage.get_token()
        if current_token is None or current_token.refresh_token is None:
            raise AuthenticationError("No refresh token available. Please re-authenticate.")

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": current_token.refresh_token,
        }

        with httpx.Client() as client:
            response = client.post(TOKEN_URL, data=data)

        if response.status_code != 200:
            error = response.json() if response.content else {}
            raise AuthenticationError(
                f"Token refresh failed: {error.get('error_description', error.get('error', 'Unknown error'))}"
            )

        token_data = response.json()
        token = TokenInfo(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token", current_token.refresh_token),
            scope=token_data.get("scope"),
        )
        self._token_storage.store_token(token)
        return token

    async def refresh_token_async(self) -> TokenInfo:
        """
        Refresh an expired access token (asynchronous).

        Returns:
            New TokenInfo with refreshed access token

        Raises:
            AuthenticationError: If no refresh token is available
        """
        current_token = self._token_storage.get_token()
        if current_token is None or current_token.refresh_token is None:
            raise AuthenticationError("No refresh token available. Please re-authenticate.")

        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": current_token.refresh_token,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(TOKEN_URL, data=data)

        if response.status_code != 200:
            error = response.json() if response.content else {}
            raise AuthenticationError(
                f"Token refresh failed: {error.get('error_description', error.get('error', 'Unknown error'))}"
            )

        token_data = response.json()
        token = TokenInfo(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            refresh_token=token_data.get("refresh_token", current_token.refresh_token),
            scope=token_data.get("scope"),
        )
        self._token_storage.store_token(token)
        return token

    def get_auth_header(self) -> dict[str, str]:
        """Get Authorization header for API requests.

        Returns:
            Dictionary with Authorization header

        Raises:
            AuthenticationError: If no valid token is available
        """
        token = self._token_storage.get_token()
        if token is None:
            raise AuthenticationError("No token available. Please authenticate first.")
        if token.is_expired:
            raise AuthenticationError("Token has expired. Please refresh or re-authenticate.")
        return {"Authorization": f"Bearer {token.access_token}"}

    def set_token(self, token: TokenInfo) -> None:
        """Manually set a token (useful for testing or pre-obtained tokens).

        Args:
            token: TokenInfo to store
        """
        self._token_storage.store_token(token)

    def clear_token(self) -> None:
        """Clear the stored token."""
        self._token_storage.clear_token()

    @staticmethod
    def _create_code_challenge(verifier: str) -> str:
        """Create S256 code challenge from verifier."""
        digest = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
