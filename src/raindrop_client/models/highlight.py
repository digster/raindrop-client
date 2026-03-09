"""Pydantic models for Raindrop.io Highlight objects.

Highlights are text annotations within a raindrop — users can mark
specific text passages with colors and optional notes.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Highlight(BaseModel):
    """A text highlight within a raindrop."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="_id", default="")
    text: str = ""
    note: str = ""
    color: str = ""
    created: datetime | None = None
    last_update: datetime | None = Field(default=None, alias="lastUpdate")
    # When listing highlights by collection, raindrop ID is included
    raindrop_id: int | None = Field(default=None, alias="raindropRef")


class HighlightCreateRequest(BaseModel):
    """Request body for adding a highlight to a raindrop."""

    text: str
    note: str = ""
    color: str = ""
