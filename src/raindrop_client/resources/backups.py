"""Resource class for Raindrop.io Backup endpoints.

Backups are snapshots of user data. The API supports listing existing backups,
triggering new backup generation, and downloading backups.
"""

from __future__ import annotations

from raindrop_client.http import HttpTransport
from raindrop_client.models.backup import Backup


class BackupsResource:
    """Manages backup operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def list(self) -> list[Backup]:
        """List all available backups."""
        data = self._transport.get("/backups")
        items = data.get("items", [])
        return [Backup.model_validate(item) for item in items]

    def generate(self) -> bool:
        """Trigger generation of a new backup.

        The backup is created asynchronously — poll list() to check when it's ready.
        """
        data = self._transport.post("/backup")
        return data.get("result", False)

    def download(self, backup_id: str) -> bytes:
        """Download a backup file.

        Args:
            backup_id: The backup ID to download.

        Returns:
            Raw bytes of the backup file.
        """
        return self._transport.download(f"/backup/{backup_id}")
