"""HTTP transport layer wrapping httpx with rate limiting, retries, and error mapping.

HttpTransport centralizes all HTTP communication with the Raindrop.io API,
handling authentication headers, rate limit backoff, and mapping HTTP status
codes to the appropriate exception types.
"""

import time
import logging
from typing import Any

import httpx

from raindrop_client.config import (
    API_BASE_URL,
    API_PREFIX,
    DEFAULT_TIMEOUT,
    RATE_LIMIT_DEFAULT_WAIT,
    RATE_LIMIT_MAX_RETRIES,
)
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

logger = logging.getLogger(__name__)

# Maps HTTP status codes to their corresponding exception class
STATUS_EXCEPTION_MAP: dict[int, type[RaindropError]] = {
    400: ValidationError,
    401: AuthenticationError,
    403: AuthorizationError,
    404: NotFoundError,
    409: ConflictError,
}


class HttpTransport:
    """Synchronous HTTP transport for Raindrop.io API.

    Handles Bearer auth, rate limit retry with backoff, and error-to-exception mapping.
    All resource classes share a single HttpTransport instance via the client facade.
    """

    def __init__(self, token: str, base_url: str = API_BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self._token = token
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    def close(self) -> None:
        """Close the underlying httpx client."""
        self._client.close()

    def _build_url(self, path: str) -> str:
        """Build full API path with version prefix."""
        if path.startswith(API_PREFIX):
            return path
        return f"{API_PREFIX}{path}"

    def _parse_rate_limit_headers(self, response: httpx.Response) -> dict[str, Any]:
        """Extract rate limit info from response headers."""
        return {
            "limit": response.headers.get("X-RateLimit-Limit"),
            "remaining": response.headers.get("X-RateLimit-Remaining"),
            "reset": response.headers.get("X-RateLimit-Reset"),
        }

    def _get_wait_time(self, response: httpx.Response) -> float:
        """Calculate wait time from rate limit Reset header (Unix timestamp)."""
        reset_ts = response.headers.get("X-RateLimit-Reset")
        if reset_ts:
            try:
                wait = float(reset_ts) - time.time()
                return max(wait, 0.5)  # At least 0.5s to avoid tight loops
            except (ValueError, TypeError):
                pass
        return RATE_LIMIT_DEFAULT_WAIT

    def _raise_for_status(self, response: httpx.Response) -> None:
        """Map HTTP error status codes to typed exceptions."""
        if response.is_success:
            return

        status = response.status_code

        # Try to parse JSON error body
        body = None
        try:
            body = response.json()
        except Exception:
            pass

        message = f"HTTP {status}"
        if body:
            # Raindrop API returns error info in various formats
            if "errorMessage" in body:
                message = body["errorMessage"]
            elif "error" in body:
                message = str(body["error"])

        # Check specific status codes first
        exc_class = STATUS_EXCEPTION_MAP.get(status)
        if exc_class:
            raise exc_class(message, status_code=status, response_body=body)

        # 5xx server errors
        if 500 <= status < 600:
            raise ServerError(message, status_code=status, response_body=body)

        # Fallback for any other error status
        raise RaindropError(message, status_code=status, response_body=body)

    def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        **kwargs,
    ) -> httpx.Response:
        """Execute an HTTP request with rate limit retry logic.

        Retries up to RATE_LIMIT_MAX_RETRIES times on 429 responses,
        sleeping based on the X-RateLimit-Reset header.
        """
        url = self._build_url(path)
        retries = 0

        while True:
            response = self._client.request(method, url, params=params, json=json_body, **kwargs)

            if response.status_code == 429:
                rate_info = self._parse_rate_limit_headers(response)
                wait_time = self._get_wait_time(response)

                if retries >= RATE_LIMIT_MAX_RETRIES:
                    raise RateLimitError(
                        f"Rate limit exceeded after {RATE_LIMIT_MAX_RETRIES} retries",
                        retry_after=wait_time,
                        status_code=429,
                        response_body=rate_info,
                    )

                retries += 1
                logger.warning(
                    "Rate limited (attempt %d/%d). Waiting %.1fs before retry.",
                    retries,
                    RATE_LIMIT_MAX_RETRIES,
                    wait_time,
                )
                time.sleep(wait_time)
                continue

            self._raise_for_status(response)
            return response

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a GET request and return parsed JSON response."""
        response = self._request("GET", path, params=params)
        return response.json()

    def post(self, path: str, json_body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a POST request and return parsed JSON response."""
        response = self._request("POST", path, params=params, json_body=json_body)
        return response.json()

    def put(self, path: str, json_body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a PUT request and return parsed JSON response."""
        response = self._request("PUT", path, params=params, json_body=json_body)
        return response.json()

    def delete(self, path: str, json_body: dict[str, Any] | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Send a DELETE request and return parsed JSON response."""
        response = self._request("DELETE", path, params=params, json_body=json_body)
        return response.json()

    def upload(self, path: str, file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> dict[str, Any]:
        """Upload a file via multipart/form-data.

        Temporarily removes the JSON content-type header for multipart requests.
        """
        url = self._build_url(path)
        files = {"file": (filename, file_data, content_type)}

        # Use a request without the default JSON content-type
        response = self._client.request(
            "PUT",
            url,
            files=files,
            headers={"Content-Type": None},  # Let httpx set multipart content-type
        )
        self._raise_for_status(response)
        return response.json()

    def upload_post(self, path: str, file_data: bytes, filename: str, field_name: str = "file", content_type: str = "application/octet-stream") -> dict[str, Any]:
        """Upload a file via POST multipart/form-data."""
        url = self._build_url(path)
        files = {field_name: (filename, file_data, content_type)}

        response = self._client.request(
            "POST",
            url,
            files=files,
            headers={"Content-Type": None},
        )
        self._raise_for_status(response)
        return response.json()

    def download(self, path: str, params: dict[str, Any] | None = None) -> bytes:
        """Download raw bytes (for exports and backup downloads)."""
        url = self._build_url(path)
        response = self._client.request("GET", url, params=params)
        self._raise_for_status(response)
        return response.content
