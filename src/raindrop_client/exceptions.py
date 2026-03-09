"""Exception hierarchy for the Raindrop.io API client.

All exceptions inherit from RaindropError, allowing callers to catch
the base class for generic error handling or specific subclasses for
targeted handling.
"""


class RaindropError(Exception):
    """Base exception for all Raindrop.io API errors."""

    def __init__(self, message: str, status_code: int | None = None, response_body: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class AuthenticationError(RaindropError):
    """Raised on 401 Unauthorized — invalid or expired token."""
    pass


class AuthorizationError(RaindropError):
    """Raised on 403 Forbidden — insufficient permissions."""
    pass


class NotFoundError(RaindropError):
    """Raised on 404 Not Found — resource does not exist."""
    pass


class ValidationError(RaindropError):
    """Raised on 400 Bad Request — invalid request parameters."""
    pass


class RateLimitError(RaindropError):
    """Raised on 429 Too Many Requests — after all retries exhausted."""

    def __init__(self, message: str, retry_after: float | None = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ConflictError(RaindropError):
    """Raised on 409 Conflict — resource state conflict."""
    pass


class ServerError(RaindropError):
    """Raised on 5xx — server-side error."""
    pass
