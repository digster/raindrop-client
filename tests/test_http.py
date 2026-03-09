"""Tests for the HTTP transport layer — rate limiting, retries, and error mapping."""

import httpx
import pytest
import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    RateLimitError,
    RaindropError,
    ServerError,
    ValidationError,
)
from raindrop_client.http import HttpTransport


BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestHttpTransport:
    """Tests for HttpTransport request handling."""

    def test_get_request(self):
        """GET requests return parsed JSON."""
        with respx.mock(base_url=BASE) as router:
            router.get("/test").respond(200, json={"result": True, "data": "hello"})
            transport = HttpTransport(token="test-token")
            result = transport.get("/test")
            assert result == {"result": True, "data": "hello"}
            transport.close()

    def test_post_request(self):
        """POST requests send JSON body and return parsed response."""
        with respx.mock(base_url=BASE) as router:
            router.post("/test").respond(200, json={"result": True})
            transport = HttpTransport(token="test-token")
            result = transport.post("/test", json_body={"key": "value"})
            assert result["result"] is True
            transport.close()

    def test_put_request(self):
        """PUT requests work correctly."""
        with respx.mock(base_url=BASE) as router:
            router.put("/test/1").respond(200, json={"result": True})
            transport = HttpTransport(token="test-token")
            result = transport.put("/test/1", json_body={"title": "updated"})
            assert result["result"] is True
            transport.close()

    def test_delete_request(self):
        """DELETE requests work correctly."""
        with respx.mock(base_url=BASE) as router:
            router.delete("/test/1").respond(200, json={"result": True})
            transport = HttpTransport(token="test-token")
            result = transport.delete("/test/1")
            assert result["result"] is True
            transport.close()

    def test_bearer_auth_header(self):
        """Transport includes Bearer token in Authorization header."""
        with respx.mock(base_url=BASE) as router:
            route = router.get("/test").respond(200, json={})
            transport = HttpTransport(token="my-secret-token")
            transport.get("/test")

            request = route.calls[0].request
            assert request.headers["authorization"] == "Bearer my-secret-token"
            transport.close()

    def test_url_building_with_prefix(self):
        """Paths already starting with API_PREFIX aren't double-prefixed."""
        transport = HttpTransport(token="test-token")
        url = transport._build_url(f"{API_PREFIX}/already")
        assert url == f"{API_PREFIX}/already"

        # Regular path gets prefix added
        url = transport._build_url("/collections")
        assert url == f"{API_PREFIX}/collections"
        transport.close()


class TestErrorMapping:
    """Tests for HTTP status code to exception mapping."""

    @pytest.mark.parametrize("status,exc_class", [
        (400, ValidationError),
        (401, AuthenticationError),
        (403, AuthorizationError),
        (404, NotFoundError),
        (409, ConflictError),
        (500, ServerError),
        (502, ServerError),
        (503, ServerError),
    ])
    def test_status_code_mapping(self, status, exc_class):
        """Each HTTP error status maps to the correct exception."""
        with respx.mock(base_url=BASE) as router:
            router.get("/fail").respond(status, json={"error": "test error"})
            transport = HttpTransport(token="test-token")
            with pytest.raises(exc_class):
                transport.get("/fail")
            transport.close()

    def test_error_includes_status_code(self):
        """Exception carries the HTTP status code."""
        with respx.mock(base_url=BASE) as router:
            router.get("/fail").respond(404, json={"error": "not found"})
            transport = HttpTransport(token="test-token")
            with pytest.raises(NotFoundError) as exc_info:
                transport.get("/fail")
            assert exc_info.value.status_code == 404
            transport.close()

    def test_error_message_from_response(self):
        """Exception message is extracted from API error response."""
        with respx.mock(base_url=BASE) as router:
            router.get("/fail").respond(400, json={"errorMessage": "Invalid field value"})
            transport = HttpTransport(token="test-token")
            with pytest.raises(ValidationError, match="Invalid field value"):
                transport.get("/fail")
            transport.close()

    def test_unknown_error_status(self):
        """Unmapped error status codes raise base RaindropError."""
        with respx.mock(base_url=BASE) as router:
            router.get("/fail").respond(418, json={"error": "I'm a teapot"})
            transport = HttpTransport(token="test-token")
            with pytest.raises(RaindropError):
                transport.get("/fail")
            transport.close()


class TestRateLimiting:
    """Tests for rate limit handling and retry logic."""

    def test_retry_on_429(self):
        """Transport retries on 429 and succeeds on next attempt."""
        import time

        with respx.mock(base_url=BASE) as router:
            # First call returns 429, second returns 200
            route = router.get("/limited")
            route.side_effect = [
                httpx.Response(429, headers={"X-RateLimit-Reset": str(time.time() + 0.1)}),
                httpx.Response(200, json={"result": True}),
            ]

            transport = HttpTransport(token="test-token")
            result = transport.get("/limited")
            assert result == {"result": True}
            assert len(route.calls) == 2
            transport.close()

    def test_rate_limit_exhausted(self):
        """RateLimitError raised after max retries exhausted."""
        import time

        with respx.mock(base_url=BASE) as router:
            # Always return 429
            route = router.get("/limited")
            route.side_effect = [
                httpx.Response(429, headers={"X-RateLimit-Reset": str(time.time() + 0.1)})
                for _ in range(4)
            ]

            transport = HttpTransport(token="test-token")
            with pytest.raises(RateLimitError, match="Rate limit exceeded"):
                transport.get("/limited")
            # 1 initial + 3 retries = 4 total calls
            assert len(route.calls) == 4
            transport.close()

    def test_rate_limit_default_wait(self):
        """Falls back to default wait time when Reset header is missing."""
        import time

        with respx.mock(base_url=BASE) as router:
            route = router.get("/limited")
            route.side_effect = [
                httpx.Response(429),  # No rate limit headers
                httpx.Response(200, json={"result": True}),
            ]

            transport = HttpTransport(token="test-token")
            # Use monkeypatch to make sleep a no-op for speed
            original_sleep = time.sleep
            time.sleep = lambda x: None
            try:
                result = transport.get("/limited")
                assert result["result"] is True
            finally:
                time.sleep = original_sleep
            transport.close()


class TestDownloadAndUpload:
    """Tests for file download and upload methods."""

    def test_download_returns_bytes(self):
        """Download returns raw bytes from response."""
        with respx.mock(base_url=BASE) as router:
            router.get("/export.csv").respond(200, content=b"col1,col2\nval1,val2")
            transport = HttpTransport(token="test-token")
            data = transport.download("/export.csv")
            assert data == b"col1,col2\nval1,val2"
            transport.close()

    def test_download_error_raises(self):
        """Download raises exception on error status."""
        with respx.mock(base_url=BASE) as router:
            router.get("/export.csv").respond(404, json={"error": "not found"})
            transport = HttpTransport(token="test-token")
            with pytest.raises(NotFoundError):
                transport.download("/export.csv")
            transport.close()
