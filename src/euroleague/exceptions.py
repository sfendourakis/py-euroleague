"""Custom exceptions for the Euroleague API client."""

from typing import Any, Optional


class EuroleagueError(Exception):
    """Base exception for all Euroleague API errors."""

    def __init__(self, message: str, *args: Any) -> None:
        self.message = message
        super().__init__(message, *args)


class AuthenticationError(EuroleagueError):
    """Authentication-related errors (401, token issues)."""

    pass


class AuthorizationError(EuroleagueError):
    """Authorization/permission errors (403)."""

    pass


class NotFoundError(EuroleagueError):
    """Resource not found (404)."""

    def __init__(self, resource_type: str, identifier: str) -> None:
        self.resource_type = resource_type
        self.identifier = identifier
        super().__init__(f"{resource_type} not found: {identifier}")


class RateLimitError(EuroleagueError):
    """Rate limit exceeded (429)."""

    def __init__(self, retry_after: Optional[int] = None) -> None:
        self.retry_after = retry_after
        message = "Rate limit exceeded"
        if retry_after:
            message += f". Retry after {retry_after} seconds"
        super().__init__(message)


class ValidationError(EuroleagueError):
    """Request validation error (400)."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None) -> None:
        self.details = details or {}
        super().__init__(message)


class APIError(EuroleagueError):
    """Generic API error with status code and response body."""

    def __init__(
        self,
        message: str,
        status_code: int,
        response_body: Optional[dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.response_body = response_body
        self.request_id = request_id
        super().__init__(f"[{status_code}] {message}")


class NetworkError(EuroleagueError):
    """Network connectivity issues."""

    pass


class TimeoutError(NetworkError):
    """Request timeout."""

    pass


def raise_for_status(status_code: int, body: dict[str, Any], headers: dict[str, str]) -> None:
    """Raise appropriate exception based on HTTP status code.

    Args:
        status_code: HTTP status code from response
        body: Parsed JSON response body
        headers: Response headers
    """
    if 200 <= status_code < 300:
        return

    message = body.get("message", body.get("error", "Unknown error"))
    request_id = headers.get("X-Request-Id")

    if status_code == 400:
        raise ValidationError(message, body.get("details"))
    elif status_code == 401:
        raise AuthenticationError(message)
    elif status_code == 403:
        raise AuthorizationError(message)
    elif status_code == 404:
        resource = body.get("resource", "Resource")
        identifier = body.get("identifier", "unknown")
        raise NotFoundError(resource, identifier)
    elif status_code == 429:
        retry_after = headers.get("Retry-After")
        raise RateLimitError(int(retry_after) if retry_after else None)
    else:
        raise APIError(message, status_code, body, request_id)
