"""Resource class for Raindrop.io Collection Sharing endpoints.

Manages collection sharing — inviting collaborators, updating access levels,
and removing collaborators.
"""

from raindrop_client.http import HttpTransport
from raindrop_client.models.sharing import Collaborator, ShareInviteRequest


class SharingResource:
    """Manages collection sharing operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def get_collaborators(self, collection_id: int) -> list[Collaborator]:
        """Get all collaborators for a shared collection."""
        data = self._transport.get(f"/collection/{collection_id}/sharing")
        items = data.get("items", [])
        return [Collaborator.model_validate(item) for item in items]

    def share(self, collection_id: int, request: ShareInviteRequest | None = None, **kwargs) -> bool:
        """Share a collection by inviting collaborators via email.

        Args:
            collection_id: The collection to share.
            request: ShareInviteRequest with role and emails.
        """
        if request is None:
            request = ShareInviteRequest(**kwargs)
        body = request.model_dump(exclude_none=True)
        data = self._transport.post(f"/collection/{collection_id}/sharing", json_body=body)
        return data.get("result", False)

    def update_access(self, collection_id: int, user_id: int, role: str) -> bool:
        """Update a collaborator's access level.

        Args:
            collection_id: The shared collection.
            user_id: The collaborator's user ID.
            role: New role — "member" (read/write) or "viewer" (read-only).
        """
        data = self._transport.put(
            f"/collection/{collection_id}/sharing/{user_id}",
            json_body={"role": role},
        )
        return data.get("result", False)

    def remove_collaborator(self, collection_id: int, user_id: int) -> bool:
        """Remove a collaborator from a shared collection."""
        data = self._transport.delete(f"/collection/{collection_id}/sharing/{user_id}")
        return data.get("result", False)

    def unshare(self, collection_id: int) -> bool:
        """Unshare a collection (remove all collaborators)."""
        data = self._transport.delete(f"/collection/{collection_id}/sharing")
        return data.get("result", False)

    def accept(self, token: str) -> bool:
        """Accept a sharing invitation.

        Args:
            token: The invitation token from the share URL.
        """
        data = self._transport.post(f"/collection/sharing/{token}")
        return data.get("result", False)
