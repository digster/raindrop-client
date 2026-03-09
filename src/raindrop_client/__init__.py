"""Raindrop.io Python API Client Library.

A typed, resource-grouped client for the Raindrop.io REST API v1.

Quick start:
    from raindrop_client import RaindropClient

    client = RaindropClient(token="your-test-token")
    collections = client.collections.list_root()
    bookmarks = client.raindrops.list(collection_id=0)
"""

__version__ = "0.1.0"

from raindrop_client.auth import OAuth2Auth, TokenResponse
from raindrop_client.client import RaindropClient
from raindrop_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    RaindropError,
    RateLimitError,
    ServerError,
    ValidationError,
)

__all__ = [
    "__version__",
    # Client
    "RaindropClient",
    # Auth
    "OAuth2Auth",
    "TokenResponse",
    # Exceptions
    "RaindropError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "ConflictError",
    "ServerError",
]
