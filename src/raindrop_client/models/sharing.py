"""Pydantic models for Raindrop.io Collection Sharing objects.

Handles collaborator info and share invitation requests for collections.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Collaborator(BaseModel):
    """A collaborator on a shared collection."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="_id", default=0)
    email: str = ""
    email_md5: str = Field(default="", alias="email_MD5")
    full_name: str = Field(default="", alias="fullName")
    registered: datetime | None = None
    role: str = ""  # "member" or "viewer"


class ShareInviteRequest(BaseModel):
    """Request body for sharing a collection with a user."""

    model_config = ConfigDict(populate_by_name=True)

    role: str = "viewer"  # "member" or "viewer"
    emails: list[str] = Field(default_factory=list)
