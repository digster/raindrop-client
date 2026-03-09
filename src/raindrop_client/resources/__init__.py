"""Resource group classes — each wraps a set of related API endpoints."""

from raindrop_client.resources.collections import CollectionsResource
from raindrop_client.resources.raindrops import RaindropsResource
from raindrop_client.resources.tags import TagsResource
from raindrop_client.resources.user import UserResource
from raindrop_client.resources.highlights import HighlightsResource
from raindrop_client.resources.filters import FiltersResource
from raindrop_client.resources.sharing import SharingResource
from raindrop_client.resources.import_export import ImportExportResource
from raindrop_client.resources.backups import BackupsResource

__all__ = [
    "CollectionsResource",
    "RaindropsResource",
    "TagsResource",
    "UserResource",
    "HighlightsResource",
    "FiltersResource",
    "SharingResource",
    "ImportExportResource",
    "BackupsResource",
]
