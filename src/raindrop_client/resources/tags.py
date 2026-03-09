"""Resource class for Raindrop.io Tag endpoints.

Tags are simple string labels. The API provides list, rename, merge, and delete.
All tag operations can be scoped to a specific collection or applied globally.
"""

from __future__ import annotations

from raindrop_client.http import HttpTransport
from raindrop_client.models.tag import Tag


class TagsResource:
    """Manages tag operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def list(self, collection_id: int | None = None) -> list[Tag]:
        """List all tags, optionally scoped to a collection.

        Args:
            collection_id: If provided, only returns tags used in this collection.
                          Use 0 for all collections.
        """
        if collection_id is not None:
            path = f"/tags/{collection_id}"
        else:
            path = "/tags"
        data = self._transport.get(path)
        items = data.get("items", [])
        return [Tag.model_validate(item) for item in items]

    def rename(self, tags: list[str], replace: str, collection_id: int | None = None) -> bool:
        """Rename one or more tags.

        Args:
            tags: List of current tag names to rename.
            replace: New tag name.
            collection_id: Scope to a specific collection.
        """
        if collection_id is not None:
            path = f"/tags/{collection_id}"
        else:
            path = "/tags"
        body = {"tags": tags, "replace": replace}
        data = self._transport.put(path, json_body=body)
        return data.get("result", False)

    def merge(self, tags: list[str], replace: str, collection_id: int | None = None) -> bool:
        """Merge multiple tags into one.

        Equivalent to rename — all source tags become the target tag.

        Args:
            tags: Tags to merge.
            replace: Target tag name.
            collection_id: Scope to a specific collection.
        """
        # Merge uses the same API endpoint as rename
        return self.rename(tags=tags, replace=replace, collection_id=collection_id)

    def delete(self, tags: list[str], collection_id: int | None = None) -> bool:
        """Delete tags from all raindrops.

        Args:
            tags: Tag names to delete.
            collection_id: Scope to a specific collection.
        """
        if collection_id is not None:
            path = f"/tags/{collection_id}"
        else:
            path = "/tags"
        body = {"tags": tags}
        data = self._transport.delete(path, json_body=body)
        return data.get("result", False)
