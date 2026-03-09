"""Resource class for Raindrop.io User endpoints.

Covers authenticated user profile, public profiles, statistics,
and connected service management.
"""

from raindrop_client.http import HttpTransport
from raindrop_client.models.user import ConnectedService, User, UserStats, UserUpdateRequest


class UserResource:
    """Manages user profile operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def get(self) -> User:
        """Get the authenticated user's profile."""
        data = self._transport.get("/user")
        return User.model_validate(data.get("user", {}))

    def update(self, request: UserUpdateRequest | None = None, **kwargs) -> User:
        """Update the authenticated user's profile.

        Can pass a UserUpdateRequest or keyword args.
        """
        if request is None:
            request = UserUpdateRequest(**kwargs)
        body = request.to_api_body()
        data = self._transport.put("/user", json_body=body)
        return User.model_validate(data.get("user", {}))

    def get_public(self, username: str) -> User:
        """Get a public user profile by username."""
        data = self._transport.get(f"/user/{username}")
        return User.model_validate(data.get("user", {}))

    def get_stats(self) -> UserStats:
        """Get account statistics (item count, trash count, pro status)."""
        data = self._transport.get("/user/stats")
        return UserStats.model_validate(data)

    def connect(self, provider: str) -> dict:
        """Connect a third-party service (Google, Dropbox, etc.).

        Returns provider-specific connection data.
        """
        return self._transport.get(f"/user/connect/{provider}")

    def disconnect(self, provider: str) -> bool:
        """Disconnect a third-party service."""
        data = self._transport.delete(f"/user/connect/{provider}")
        return data.get("result", False)
