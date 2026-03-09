"""Resource class for Raindrop.io Highlight endpoints.

Highlights are text annotations within raindrops. This resource handles
listing highlights across collections and individual raindrops.
"""

from __future__ import annotations

from raindrop_client.http import HttpTransport
from raindrop_client.models.highlight import Highlight


class HighlightsResource:
    """Manages highlight operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def list(self, raindrop_id: int) -> list[Highlight]:
        """List all highlights for a specific raindrop.

        Args:
            raindrop_id: The raindrop to get highlights from.
        """
        data = self._transport.get(f"/raindrop/{raindrop_id}")
        item = data.get("item", {})
        highlights_data = item.get("highlights", [])
        return [Highlight.model_validate(h) for h in highlights_data]

    def list_by_collection(self, collection_id: int = 0, page: int = 0) -> list[Highlight]:
        """List all highlights across raindrops in a collection.

        Args:
            collection_id: Collection ID. Use 0 for all collections.
            page: Page number (0-indexed).
        """
        params = {"page": page}
        data = self._transport.get(f"/highlights/{collection_id}", params=params)
        items = data.get("items", [])
        return [Highlight.model_validate(h) for h in items]
