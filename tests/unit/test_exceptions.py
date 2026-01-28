"""Unit tests for exceptions module."""

import pytest

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
    raise_for_status,
)


class TestEuroleagueError:
    """Tests for base exception class."""

    def test_message_attribute(self):
        """Exception should store message attribute."""
        error = EuroleagueError("Test error")
        assert error.message == "Test error"
        assert str(error) == "Test error"


class TestAuthenticationError:
    """Tests for authentication error."""

    def test_inherits_from_base(self):
        """AuthenticationError should inherit from EuroleagueError."""
        error = AuthenticationError("Invalid token")
        assert isinstance(error, EuroleagueError)
        assert error.message == "Invalid token"


class TestAuthorizationError:
    """Tests for authorization error."""

    def test_inherits_from_base(self):
        """AuthorizationError should inherit from EuroleagueError."""
        error = AuthorizationError("Access denied")
        assert isinstance(error, EuroleagueError)
        assert error.message == "Access denied"


class TestNotFoundError:
    """Tests for not found error."""

    def test_stores_resource_info(self):
        """NotFoundError should store resource type and identifier."""
        error = NotFoundError("Club", "BAR")
        assert error.resource_type == "Club"
        assert error.identifier == "BAR"
        assert "Club not found: BAR" in str(error)

    def test_inherits_from_base(self):
        """NotFoundError should inherit from EuroleagueError."""
        error = NotFoundError("Player", "P001")
        assert isinstance(error, EuroleagueError)


class TestRateLimitError:
    """Tests for rate limit error."""

    def test_without_retry_after(self):
        """RateLimitError should work without retry_after."""
        error = RateLimitError()
        assert error.retry_after is None
        assert "Rate limit exceeded" in str(error)

    def test_with_retry_after(self):
        """RateLimitError should include retry_after in message."""
        error = RateLimitError(retry_after=60)
        assert error.retry_after == 60
        assert "60 seconds" in str(error)


class TestValidationError:
    """Tests for validation error."""

    def test_stores_details(self):
        """ValidationError should store details dict."""
        details = {"field": "season_code", "error": "invalid format"}
        error = ValidationError("Invalid request", details=details)
        assert error.details == details
        assert error.message == "Invalid request"

    def test_default_empty_details(self):
        """ValidationError should have empty dict by default."""
        error = ValidationError("Invalid request")
        assert error.details == {}


class TestAPIError:
    """Tests for generic API error."""

    def test_stores_all_attributes(self):
        """APIError should store all attributes."""
        body = {"error": "Something went wrong"}
        error = APIError(
            message="Server error",
            status_code=500,
            response_body=body,
            request_id="req-123",
        )
        assert error.status_code == 500
        assert error.response_body == body
        assert error.request_id == "req-123"
        assert "[500]" in str(error)
        assert "Server error" in str(error)

    def test_optional_attributes(self):
        """APIError should work with optional attributes."""
        error = APIError("Error", status_code=500)
        assert error.response_body is None
        assert error.request_id is None


class TestNetworkError:
    """Tests for network error."""

    def test_inherits_from_base(self):
        """NetworkError should inherit from EuroleagueError."""
        error = NetworkError("Connection refused")
        assert isinstance(error, EuroleagueError)


class TestTimeoutError:
    """Tests for timeout error."""

    def test_inherits_from_network_error(self):
        """TimeoutError should inherit from NetworkError."""
        error = TimeoutError("Request timed out")
        assert isinstance(error, NetworkError)
        assert isinstance(error, EuroleagueError)


class TestRaiseForStatus:
    """Tests for raise_for_status function."""

    def test_success_codes_no_exception(self):
        """Should not raise for 2xx status codes."""
        for code in [200, 201, 204]:
            raise_for_status(code, {}, {})  # Should not raise

    def test_400_raises_validation_error(self):
        """Should raise ValidationError for 400."""
        with pytest.raises(ValidationError) as exc_info:
            raise_for_status(
                400,
                {"message": "Invalid parameter", "details": {"field": "limit"}},
                {},
            )
        assert exc_info.value.message == "Invalid parameter"
        assert exc_info.value.details == {"field": "limit"}

    def test_401_raises_authentication_error(self):
        """Should raise AuthenticationError for 401."""
        with pytest.raises(AuthenticationError) as exc_info:
            raise_for_status(401, {"message": "Invalid token"}, {})
        assert exc_info.value.message == "Invalid token"

    def test_403_raises_authorization_error(self):
        """Should raise AuthorizationError for 403."""
        with pytest.raises(AuthorizationError) as exc_info:
            raise_for_status(403, {"message": "Access denied"}, {})
        assert exc_info.value.message == "Access denied"

    def test_404_raises_not_found_error(self):
        """Should raise NotFoundError for 404."""
        with pytest.raises(NotFoundError) as exc_info:
            raise_for_status(
                404,
                {"resource": "Club", "identifier": "INVALID"},
                {},
            )
        assert exc_info.value.resource_type == "Club"
        assert exc_info.value.identifier == "INVALID"

    def test_404_with_defaults(self):
        """Should use defaults for 404 without resource info."""
        with pytest.raises(NotFoundError) as exc_info:
            raise_for_status(404, {}, {})
        assert exc_info.value.resource_type == "Resource"
        assert exc_info.value.identifier == "unknown"

    def test_429_raises_rate_limit_error(self):
        """Should raise RateLimitError for 429."""
        with pytest.raises(RateLimitError) as exc_info:
            raise_for_status(429, {}, {"Retry-After": "60"})
        assert exc_info.value.retry_after == 60

    def test_429_without_retry_after(self):
        """Should raise RateLimitError without retry_after header."""
        with pytest.raises(RateLimitError) as exc_info:
            raise_for_status(429, {}, {})
        assert exc_info.value.retry_after is None

    def test_500_raises_api_error(self):
        """Should raise APIError for 500."""
        with pytest.raises(APIError) as exc_info:
            raise_for_status(
                500,
                {"message": "Internal error"},
                {"X-Request-Id": "req-123"},
            )
        assert exc_info.value.status_code == 500
        assert exc_info.value.request_id == "req-123"

    def test_uses_error_field_as_fallback(self):
        """Should use 'error' field if 'message' not present."""
        with pytest.raises(APIError) as exc_info:
            raise_for_status(500, {"error": "Something went wrong"}, {})
        assert "Something went wrong" in str(exc_info.value)

    def test_unknown_error_fallback(self):
        """Should use 'Unknown error' if no message fields present."""
        with pytest.raises(APIError) as exc_info:
            raise_for_status(500, {}, {})
        assert "Unknown error" in str(exc_info.value)
