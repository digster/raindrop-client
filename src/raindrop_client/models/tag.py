"""Pydantic models for Raindrop.io Tag objects.

Tags are simple string labels attached to raindrops. The API returns them
with a count of how many raindrops use each tag.
"""

from pydantic import BaseModel, ConfigDict, Field


class Tag(BaseModel):
    """A tag with its usage count."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    tag: str = Field(alias="_id", default="")
    count: int = 0


class TagRenameRequest(BaseModel):
    """Request body for renaming tags."""

    replace: str  # New tag name
    tags: list[str]  # Old tag names to replace


class TagMergeRequest(BaseModel):
    """Request body for merging multiple tags into one."""

    replace: str  # Target tag name
    tags: list[str]  # Tags to merge into the target


class TagDeleteRequest(BaseModel):
    """Request body for deleting tags."""

    tags: list[str]  # Tags to delete
