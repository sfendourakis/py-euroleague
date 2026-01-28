"""Unit tests for HTTP client module."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from euroleague.exceptions import APIError, NetworkError, TimeoutError
from euroleague.http import AsyncHTTPClient, HTTPClient, _calculate_backoff


class TestCalculateBackoff:
    """Tests for exponential backoff calculation."""

    def test_first_attempt(self):
        """First attempt should use base delay."""
        assert _calculate_backoff(0) == 0.5

    def test_second_attempt(self):
        """Second attempt should double the delay."""
        assert _calculate_backoff(1) == 1.0

    def test_third_attempt(self):
        """Third attempt should quadruple the base delay."""
        assert _calculate_backoff(2) == 2.0

    def test_max_delay_cap(self):
        """Delay should be capped at max_delay."""
        # With base_delay=0.5, attempt 10 would be 0.5 * 2^10 = 512
        assert _calculate_backoff(10) == 30.0

    def test_custom_base_delay(self):
        """Custom base delay should work."""
        assert _calculate_backoff(0, base_delay=1.0) == 1.0
        assert _calculate_backoff(1, base_delay=1.0) == 2.0

    def test_custom_max_delay(self):
        """Custom max delay should work."""
        assert _calculate_backoff(10, max_delay=10.0) == 10.0


class TestHTTPClient:
    """Tests for synchronous HTTP client."""

    def test_requires_https(self):
        """Client should reject non-HTTPS URLs."""
        with pytest.raises(ValueError, match="must use HTTPS"):
            HTTPClient(base_url="http://example.com")

    def test_initialization(self):
        """Client should initialize with correct settings."""
        client = HTTPClient(
            base_url="https://api.example.com",
            timeout=60.0,
            max_retries=5,
        )
        assert client._base_url == "https://api.example.com"
        assert client._timeout == 60.0
        assert client._max_retries == 5
        client.close()

    def test_strips_trailing_slash(self):
        """Client should strip trailing slash from base URL."""
        client = HTTPClient(base_url="https://api.example.com/")
        assert client._base_url == "https://api.example.com"
        client.close()

    @patch("euroleague.http.httpx.Client")
    def test_successful_get(self, mock_client_class):
        """Client should return parsed JSON on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {}

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = HTTPClient()
        result = client.get("/test")

        assert result == {"data": "test"}
        client.close()

    @patch("euroleague.http.httpx.Client")
    def test_filters_none_params(self, mock_client_class):
        """Client should filter out None values from params."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"{}"
        mock_response.json.return_value = {}
        mock_response.headers = {}

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = HTTPClient()
        client.get("/test", params={"a": 1, "b": None, "c": "value"})

        # Check that the call was made with filtered params
        call_args = mock_client.get.call_args
        assert call_args[1]["params"] == {"a": 1, "c": "value"}
        client.close()

    @patch("euroleague.http.httpx.Client")
    def test_invalid_json_response(self, mock_client_class):
        """Client should raise APIError for invalid JSON."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"not json"
        mock_response.text = "not json"
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = HTTPClient()
        with pytest.raises(APIError, match="Invalid JSON"):
            client.get("/test")
        client.close()

    @patch("euroleague.http.time.sleep")
    @patch("euroleague.http.httpx.Client")
    def test_retry_on_timeout(self, mock_client_class, mock_sleep):
        """Client should retry on timeout."""
        mock_client = MagicMock()
        mock_client.get.side_effect = [
            httpx.TimeoutException("timeout"),
            httpx.TimeoutException("timeout"),
            MagicMock(
                status_code=200,
                content=b'{"data": "success"}',
                json=MagicMock(return_value={"data": "success"}),
                headers={},
            ),
        ]
        mock_client_class.return_value = mock_client

        client = HTTPClient(max_retries=3)
        result = client.get("/test")

        assert result == {"data": "success"}
        assert mock_client.get.call_count == 3
        assert mock_sleep.call_count == 2
        client.close()

    @patch("euroleague.http.time.sleep")
    @patch("euroleague.http.httpx.Client")
    def test_timeout_after_all_retries(self, mock_client_class, mock_sleep):
        """Client should raise TimeoutError after all retries exhausted."""
        mock_client = MagicMock()
        mock_client.get.side_effect = httpx.TimeoutException("timeout")
        mock_client_class.return_value = mock_client

        client = HTTPClient(max_retries=3)
        with pytest.raises(TimeoutError, match="Request timed out"):
            client.get("/test")

        assert mock_client.get.call_count == 3
        client.close()

    @patch("euroleague.http.time.sleep")
    @patch("euroleague.http.httpx.Client")
    def test_retry_on_network_error(self, mock_client_class, mock_sleep):
        """Client should retry on network error."""
        mock_client = MagicMock()
        mock_client.get.side_effect = [
            httpx.NetworkError("connection failed"),
            MagicMock(
                status_code=200,
                content=b'{"data": "success"}',
                json=MagicMock(return_value={"data": "success"}),
                headers={},
            ),
        ]
        mock_client_class.return_value = mock_client

        client = HTTPClient(max_retries=3)
        result = client.get("/test")

        assert result == {"data": "success"}
        assert mock_client.get.call_count == 2
        client.close()

    @patch("euroleague.http.time.sleep")
    @patch("euroleague.http.httpx.Client")
    def test_network_error_after_all_retries(self, mock_client_class, mock_sleep):
        """Client should raise NetworkError after all retries exhausted."""
        mock_client = MagicMock()
        mock_client.get.side_effect = httpx.NetworkError("connection failed")
        mock_client_class.return_value = mock_client

        client = HTTPClient(max_retries=3)
        with pytest.raises(NetworkError, match="connection failed"):
            client.get("/test")

        assert mock_client.get.call_count == 3
        client.close()


class TestAsyncHTTPClient:
    """Tests for asynchronous HTTP client."""

    def test_requires_https(self):
        """Client should reject non-HTTPS URLs."""
        with pytest.raises(ValueError, match="must use HTTPS"):
            AsyncHTTPClient(base_url="http://example.com")

    def test_initialization(self):
        """Client should initialize with correct settings."""
        client = AsyncHTTPClient(
            base_url="https://api.example.com",
            timeout=60.0,
            max_retries=5,
        )
        assert client._base_url == "https://api.example.com"
        assert client._timeout == 60.0
        assert client._max_retries == 5

    @pytest.mark.asyncio
    async def test_successful_get(self):
        """Client should return parsed JSON on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"data": "test"}'
        mock_response.json.return_value = {"data": "test"}
        mock_response.headers = {}

        with patch("euroleague.http.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get.return_value = mock_response
            mock_client_class.return_value = mock_client

            client = AsyncHTTPClient()
            result = await client.get("/test")

            assert result == {"data": "test"}
            await client.close()

    @pytest.mark.asyncio
    async def test_retry_on_timeout(self):
        """Client should retry on timeout."""
        with patch("euroleague.http.httpx.AsyncClient") as mock_client_class:
            with patch("euroleague.http.asyncio.sleep", new_callable=AsyncMock):
                mock_client = AsyncMock()
                mock_client.get.side_effect = [
                    httpx.TimeoutException("timeout"),
                    MagicMock(
                        status_code=200,
                        content=b'{"data": "success"}',
                        json=MagicMock(return_value={"data": "success"}),
                        headers={},
                    ),
                ]
                mock_client_class.return_value = mock_client

                client = AsyncHTTPClient(max_retries=3)
                result = await client.get("/test")

                assert result == {"data": "success"}
                assert mock_client.get.call_count == 2
                await client.close()

    @pytest.mark.asyncio
    async def test_timeout_after_all_retries(self):
        """Client should raise TimeoutError after all retries exhausted."""
        with patch("euroleague.http.httpx.AsyncClient") as mock_client_class:
            with patch("euroleague.http.asyncio.sleep", new_callable=AsyncMock):
                mock_client = AsyncMock()
                mock_client.get.side_effect = httpx.TimeoutException("timeout")
                mock_client_class.return_value = mock_client

                client = AsyncHTTPClient(max_retries=3)
                with pytest.raises(TimeoutError, match="Request timed out"):
                    await client.get("/test")

                assert mock_client.get.call_count == 3
                await client.close()
