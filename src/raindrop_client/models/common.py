"""Shared types used across multiple model modules.

These are the building blocks that collection, raindrop, and other models
reference — kept separate to avoid circular imports.
"""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class CollectionRef(BaseModel):
    """Reference to a collection, using Raindrop's $id convention."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="$id")


class AccessLevel(BaseModel):
    """Access level indicator for a collection."""

    model_config = ConfigDict(extra="ignore")

    level: int = 0
    draggable: bool = True


class View(StrEnum):
    """Display view modes for collections."""

    LIST = "list"
    SIMPLE = "simple"
    GRID = "grid"
    MASONRY = "masonry"
    HEADLINES = "headlines"


class RaindropType(StrEnum):
    """Content types for raindrops."""

    LINK = "link"
    ARTICLE = "article"
    IMAGE = "image"
    VIDEO = "video"
    DOCUMENT = "document"
    AUDIO = "audio"


class MediaItem(BaseModel):
    """Media item attached to a raindrop (image, screenshot, etc.)."""

    model_config = ConfigDict(extra="ignore")

    link: str = ""
    type: str = ""


class UserRef(BaseModel):
    """Reference to a user by ID."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="$id", default=0)


class Creator(BaseModel):
    """Creator reference embedded in various API objects."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="_id", default=0)
    full_name: str = Field(default="", alias="fullName")
    avatar: str = ""
