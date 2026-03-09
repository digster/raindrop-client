"""Resource class for Raindrop.io Filter endpoints.

Filters provide aggregated counts (by tag, type, broken links, etc.)
for a collection — useful for building faceted search UIs.
"""

from raindrop_client.http import HttpTransport
from raindrop_client.models.filter import FilterCounts


class FiltersResource:
    """Manages filter (facet count) operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def get(self, collection_id: int = 0, tags_sort: str | None = None, search: str | None = None) -> FilterCounts:
        """Get filter counts for a collection.

        Args:
            collection_id: Collection ID. Use 0 for all collections.
            tags_sort: Sort tags by "-count" (default) or "_id" (by name).
            search: Filter by search query.
        """
        params: dict = {}
        if tags_sort:
            params["tagsSort"] = tags_sort
        if search:
            params["search"] = search

        data = self._transport.get(f"/filters/{collection_id}", params=params if params else None)
        return FilterCounts.model_validate(data)
