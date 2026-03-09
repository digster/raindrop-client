"""Resource class for Raindrop.io Raindrop (bookmark) endpoints.

Covers single and bulk CRUD, file/cover uploads, suggestions, and cache retrieval.
"""

from __future__ import annotations

from raindrop_client.config import DEFAULT_PER_PAGE
from raindrop_client.http import HttpTransport
from raindrop_client.models.raindrop import Raindrop, RaindropCreateRequest, RaindropSuggestion, RaindropUpdateRequest


class RaindropsResource:
    """Manages raindrop (bookmark) operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def get(self, raindrop_id: int) -> Raindrop:
        """Get a single raindrop by ID."""
        data = self._transport.get(f"/raindrop/{raindrop_id}")
        return Raindrop.model_validate(data.get("item", {}))

    def create(self, request: RaindropCreateRequest | None = None, **kwargs) -> Raindrop:
        """Create a new raindrop (bookmark).

        Can pass a RaindropCreateRequest or keyword args (link, title, tags, etc.).
        """
        if request is None:
            request = RaindropCreateRequest(**kwargs)
        body = request.to_api_body()
        data = self._transport.post("/raindrop", json_body=body)
        return Raindrop.model_validate(data.get("item", {}))

    def update(self, raindrop_id: int, request: RaindropUpdateRequest | None = None, **kwargs) -> Raindrop:
        """Update an existing raindrop.

        Can pass a RaindropUpdateRequest or keyword args.
        """
        if request is None:
            request = RaindropUpdateRequest(**kwargs)
        body = request.to_api_body()
        data = self._transport.put(f"/raindrop/{raindrop_id}", json_body=body)
        return Raindrop.model_validate(data.get("item", {}))

    def delete(self, raindrop_id: int) -> bool:
        """Delete a raindrop (moves to Trash, or permanently if already in Trash)."""
        data = self._transport.delete(f"/raindrop/{raindrop_id}")
        return data.get("result", False)

    def list(
        self,
        collection_id: int = 0,
        search: str | None = None,
        sort: str | None = None,
        page: int = 0,
        perpage: int = DEFAULT_PER_PAGE,
        nested: bool | None = None,
    ) -> list[Raindrop]:
        """List raindrops in a collection with optional filtering and pagination.

        Args:
            collection_id: Collection to list from. 0 = all, -1 = unsorted, -99 = trash.
            search: Search query string.
            sort: Sort order (e.g., "-created", "title", "-sort", "score").
            page: Page number (0-indexed).
            perpage: Items per page (max 50).
            nested: Whether to include raindrops from nested collections.
        """
        params: dict = {"page": page, "perpage": perpage}
        if search:
            params["search"] = search
        if sort:
            params["sort"] = sort
        if nested is not None:
            params["nested"] = str(nested).lower()

        data = self._transport.get(f"/raindrops/{collection_id}", params=params)
        items = data.get("items", [])
        return [Raindrop.model_validate(item) for item in items]

    def create_many(self, items: list[dict]) -> list[Raindrop]:
        """Create multiple raindrops at once.

        Args:
            items: List of raindrop data dicts (each should have at least "link").
        """
        data = self._transport.post("/raindrops", json_body={"items": items})
        return [Raindrop.model_validate(item) for item in data.get("items", [])]

    def update_many(
        self,
        ids: list[int] | None = None,
        collection_id: int | None = None,
        search: str | None = None,
        **updates,
    ) -> dict:
        """Update multiple raindrops at once.

        Args:
            ids: Specific raindrop IDs to update.
            collection_id: Update all in this collection (use with search for filtering).
            search: Limit updates to matching raindrops.
            **updates: Fields to update (tags, important, collection, etc.).
        """
        body: dict = {}
        if ids:
            body["ids"] = ids
        body.update(updates)

        path = f"/raindrops/{collection_id}" if collection_id is not None else "/raindrops/0"
        params = {"search": search} if search else None
        data = self._transport.put(path, json_body=body, params=params)
        return {"result": data.get("result", False), "modified": data.get("modified", 0)}

    def delete_many(
        self,
        collection_id: int = 0,
        ids: list[int] | None = None,
        search: str | None = None,
        nested: bool | None = None,
    ) -> dict:
        """Delete multiple raindrops.

        Args:
            collection_id: Collection to delete from. Use -99 for permanent deletion.
            ids: Specific IDs to delete.
            search: Limit deletion to matching raindrops.
            nested: Include nested collections.
        """
        body = {}
        if ids:
            body["ids"] = ids

        params: dict = {}
        if search:
            params["search"] = search
        if nested is not None:
            params["nested"] = str(nested).lower()

        data = self._transport.delete(
            f"/raindrops/{collection_id}",
            json_body=body if body else None,
            params=params if params else None,
        )
        return {"result": data.get("result", False), "modified": data.get("modified", 0)}

    def upload_file(self, collection_id: int, file_data: bytes, filename: str, content_type: str = "application/octet-stream") -> Raindrop:
        """Upload a file as a new raindrop (PDF, image, etc.).

        Args:
            collection_id: Collection to upload into.
            file_data: Raw file bytes.
            filename: Original filename.
            content_type: MIME type of the file.
        """
        data = self._transport.upload(f"/raindrop/file", file_data, filename, content_type)
        return Raindrop.model_validate(data.get("item", {}))

    def upload_cover(self, raindrop_id: int, file_data: bytes, filename: str, content_type: str = "image/jpeg") -> Raindrop:
        """Upload a custom cover image for a raindrop."""
        data = self._transport.upload(f"/raindrop/{raindrop_id}/cover", file_data, filename, content_type)
        return Raindrop.model_validate(data.get("item", {}))

    def get_cache(self, raindrop_id: int) -> bytes:
        """Download the permanent copy (cache) of a raindrop.

        Returns raw bytes of the cached page content.
        """
        return self._transport.download(f"/raindrop/{raindrop_id}/cache")

    def suggest_for_url(self, link: str) -> RaindropSuggestion:
        """Get suggested collections and tags for a new bookmark URL."""
        data = self._transport.post("/raindrop/suggest", json_body={"link": link})
        return RaindropSuggestion.model_validate(data.get("item", {}))

    def suggest_for_existing(self, raindrop_id: int) -> RaindropSuggestion:
        """Get suggested collections and tags for an existing raindrop."""
        data = self._transport.get(f"/raindrop/{raindrop_id}/suggest")
        return RaindropSuggestion.model_validate(data.get("item", {}))
