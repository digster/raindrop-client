"""Pydantic models for Raindrop.io Collection objects.

Collections are folders that organize raindrops (bookmarks). They support
nesting via parent references, custom cover images, and sharing.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from raindrop_client.models.common import AccessLevel, CollectionRef, UserRef, View


class Collection(BaseModel):
    """A Raindrop.io collection (folder for bookmarks).

    Special collection IDs:
      - 0:   All raindrops
      - -1:  Unsorted
      - -99: Trash
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="_id", default=0)
    title: str = ""
    description: str = ""
    color: str = ""
    cover: list[str] = Field(default_factory=list)
    count: int = 0
    view: str = Field(default="list")
    public: bool = False
    expanded: bool = True
    sort: int = 0
    parent: CollectionRef | None = None
    user: UserRef | None = None
    access: AccessLevel = Field(default_factory=AccessLevel)
    collaborators: list[dict] | None = None
    created: datetime | None = None
    last_update: datetime | None = Field(default=None, alias="lastUpdate")
    slug: str = ""
    note: str = ""


class CollectionCreateRequest(BaseModel):
    """Request body for creating a new collection."""

    model_config = ConfigDict(populate_by_name=True)

    title: str
    view: str | None = None
    public: bool | None = None
    sort: int | None = None
    cover: list[str] | None = None
    parent_id: int | None = Field(default=None, exclude=True)

    def to_api_body(self) -> dict:
        """Convert to API request format, handling parent.$id nesting."""
        body = self.model_dump(exclude_none=True, exclude={"parent_id"})
        if self.parent_id is not None:
            body["parent"] = {"$id": self.parent_id}
        return body


class CollectionUpdateRequest(BaseModel):
    """Request body for updating an existing collection."""

    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    description: str | None = None
    view: str | None = None
    public: bool | None = None
    sort: int | None = None
    expanded: bool | None = None
    cover: list[str] | None = None
    color: str | None = None
    parent_id: int | None = Field(default=None, exclude=True)

    def to_api_body(self) -> dict:
        """Convert to API request format, handling parent.$id nesting."""
        body = self.model_dump(exclude_none=True, exclude={"parent_id"})
        if self.parent_id is not None:
            body["parent"] = {"$id": self.parent_id}
        return body
