"""Pydantic models for all Raindrop.io API entities."""

from raindrop_client.models.common import CollectionRef, AccessLevel, View, RaindropType, MediaItem
from raindrop_client.models.collection import Collection, CollectionCreateRequest, CollectionUpdateRequest
from raindrop_client.models.raindrop import (
    Raindrop,
    RaindropCreateRequest,
    RaindropUpdateRequest,
    RaindropSuggestion,
    CacheStatus,
)
from raindrop_client.models.tag import Tag, TagRenameRequest, TagMergeRequest, TagDeleteRequest
from raindrop_client.models.user import User, UserStats, UserUpdateRequest, ConnectedService
from raindrop_client.models.highlight import Highlight, HighlightCreateRequest
from raindrop_client.models.filter import FilterCounts, FilterTagItem, FilterTypeItem
from raindrop_client.models.backup import Backup
from raindrop_client.models.sharing import Collaborator, ShareInviteRequest

__all__ = [
    # Common
    "CollectionRef",
    "AccessLevel",
    "View",
    "RaindropType",
    "MediaItem",
    # Collection
    "Collection",
    "CollectionCreateRequest",
    "CollectionUpdateRequest",
    # Raindrop
    "Raindrop",
    "RaindropCreateRequest",
    "RaindropUpdateRequest",
    "RaindropSuggestion",
    "CacheStatus",
    # Tag
    "Tag",
    "TagRenameRequest",
    "TagMergeRequest",
    "TagDeleteRequest",
    # User
    "User",
    "UserStats",
    "UserUpdateRequest",
    "ConnectedService",
    # Highlight
    "Highlight",
    "HighlightCreateRequest",
    # Filter
    "FilterCounts",
    "FilterTagItem",
    "FilterTypeItem",
    # Backup
    "Backup",
    # Sharing
    "Collaborator",
    "ShareInviteRequest",
]
