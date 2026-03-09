"""Pydantic models for Raindrop.io Raindrop (bookmark) objects.

Raindrops are the core entity — each represents a saved bookmark with
metadata like tags, highlights, cover images, and cache status.
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from raindrop_client.models.common import CollectionRef, Creator, MediaItem, RaindropType


class CacheStatus(StrEnum):
    """Permanent copy (cache) creation status."""

    READY = "ready"
    RETRY = "retry"
    FAILED = "failed"
    INVALID_ORIGIN = "invalid-origin"
    INVALID_TIMEOUT = "invalid-timeout"


class RaindropCache(BaseModel):
    """Cache (permanent copy) info for a raindrop."""

    model_config = ConfigDict(extra="ignore")

    status: str = ""
    size: int = 0
    created: datetime | None = None


class RaindropFile(BaseModel):
    """File attachment info for file-type raindrops."""

    model_config = ConfigDict(extra="ignore")

    name: str = ""
    size: int = 0
    type: str = ""


class Raindrop(BaseModel):
    """A Raindrop.io raindrop (bookmark).

    The collection field uses Raindrop's $id reference format.
    Use `collection.id` to get the numeric collection ID.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="_id", default=0)
    link: str = ""
    title: str = ""
    excerpt: str = ""
    note: str = ""
    type: str = Field(default="link")
    cover: str = ""
    tags: list[str] = Field(default_factory=list)
    important: bool = False
    removed: bool = False
    domain: str = ""
    collection: CollectionRef | None = None
    creator: Creator | None = None
    media: list[MediaItem] = Field(default_factory=list)
    highlights: list[dict] = Field(default_factory=list)
    cache: RaindropCache | None = None
    file: RaindropFile | None = None
    created: datetime | None = None
    last_update: datetime | None = Field(default=None, alias="lastUpdate")
    order: int = 0
    please_parse: dict | None = Field(default=None, alias="pleaseParse")


class RaindropCreateRequest(BaseModel):
    """Request body for creating a new raindrop."""

    model_config = ConfigDict(populate_by_name=True)

    link: str
    title: str | None = None
    excerpt: str | None = None
    note: str | None = None
    tags: list[str] | None = None
    important: bool | None = None
    collection_id: int | None = Field(default=None, exclude=True)
    cover: str | None = None
    type: str | None = None
    order: int | None = None
    please_parse: bool | None = Field(default=None, exclude=True)
    media: list[dict] | None = None
    highlights: list[dict] | None = None

    def to_api_body(self) -> dict:
        """Convert to API request format, handling collection.$id and pleaseParse."""
        body = self.model_dump(exclude_none=True, exclude={"collection_id", "please_parse"})
        if self.collection_id is not None:
            body["collection"] = {"$id": self.collection_id}
        if self.please_parse is not None:
            body["pleaseParse"] = {}
        return body


class RaindropUpdateRequest(BaseModel):
    """Request body for updating an existing raindrop."""

    model_config = ConfigDict(populate_by_name=True)

    link: str | None = None
    title: str | None = None
    excerpt: str | None = None
    note: str | None = None
    tags: list[str] | None = None
    important: bool | None = None
    collection_id: int | None = Field(default=None, exclude=True)
    cover: str | None = None
    type: str | None = None
    order: int | None = None
    media: list[dict] | None = None
    highlights: list[dict] | None = None

    def to_api_body(self) -> dict:
        """Convert to API request format, handling collection.$id."""
        body = self.model_dump(exclude_none=True, exclude={"collection_id"})
        if self.collection_id is not None:
            body["collection"] = {"$id": self.collection_id}
        return body


class RaindropSuggestion(BaseModel):
    """Suggested collections and tags for a bookmark URL."""

    model_config = ConfigDict(extra="ignore")

    collections: list[CollectionRef] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
