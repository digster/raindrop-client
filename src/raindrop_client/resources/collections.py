"""Resource class for Raindrop.io Collection endpoints.

Covers CRUD operations, cover uploads, bulk operations (reorder, merge, clean),
and special operations like emptying trash.
"""

from raindrop_client.http import HttpTransport
from raindrop_client.models.collection import Collection, CollectionCreateRequest, CollectionUpdateRequest


class CollectionsResource:
    """Manages collection (folder) operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def list_root(self) -> list[Collection]:
        """List all root-level collections."""
        data = self._transport.get("/collections")
        items = data.get("items", [])
        return [Collection.model_validate(item) for item in items]

    def list_children(self) -> list[Collection]:
        """List all child (nested) collections."""
        data = self._transport.get("/childrens")
        items = data.get("items", [])
        return [Collection.model_validate(item) for item in items]

    def get(self, collection_id: int) -> Collection:
        """Get a single collection by ID."""
        data = self._transport.get(f"/collection/{collection_id}")
        return Collection.model_validate(data.get("item", {}))

    def create(self, request: CollectionCreateRequest | None = None, **kwargs) -> Collection:
        """Create a new collection.

        Can pass a CollectionCreateRequest or keyword args (title, view, public, etc.).
        """
        if request is None:
            request = CollectionCreateRequest(**kwargs)
        body = request.to_api_body()
        data = self._transport.post("/collection", json_body=body)
        return Collection.model_validate(data.get("item", {}))

    def update(self, collection_id: int, request: CollectionUpdateRequest | None = None, **kwargs) -> Collection:
        """Update an existing collection.

        Can pass a CollectionUpdateRequest or keyword args.
        """
        if request is None:
            request = CollectionUpdateRequest(**kwargs)
        body = request.to_api_body()
        data = self._transport.put(f"/collection/{collection_id}", json_body=body)
        return Collection.model_validate(data.get("item", {}))

    def delete(self, collection_id: int) -> bool:
        """Delete a collection. Moves raindrops to Trash."""
        data = self._transport.delete(f"/collection/{collection_id}")
        return data.get("result", False)

    def upload_cover(self, collection_id: int, file_data: bytes, filename: str, content_type: str = "image/jpeg") -> Collection:
        """Upload a custom cover image for a collection."""
        data = self._transport.upload(f"/collection/{collection_id}/cover", file_data, filename, content_type)
        return Collection.model_validate(data.get("item", {}))

    def delete_many(self, collection_ids: list[int]) -> bool:
        """Delete multiple collections at once."""
        data = self._transport.delete("/collections", json_body={"ids": collection_ids})
        return data.get("result", False)

    def reorder(self, sort: str = "title") -> bool:
        """Reorder all collections.

        Args:
            sort: Sort method — "title" (alphabetical) or "-count" (by raindrop count).
        """
        data = self._transport.put("/collections", json_body={"sort": sort})
        return data.get("result", False)

    def empty_trash(self) -> bool:
        """Permanently delete all items in the Trash collection."""
        data = self._transport.delete("/collection/-99")
        return data.get("result", False)

    def merge(self, collection_ids: list[int], to: int) -> bool:
        """Merge multiple collections into one.

        Args:
            collection_ids: Source collection IDs to merge from.
            to: Target collection ID to merge into.
        """
        data = self._transport.put("/collections/merge", json_body={"ids": collection_ids, "to": to})
        return data.get("result", False)

    def clean(self, collection_id: int) -> bool:
        """Remove all empty sub-collections from a parent collection."""
        data = self._transport.put(f"/collection/{collection_id}/clean")
        return data.get("result", False)
