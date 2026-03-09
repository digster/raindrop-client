"""Pydantic models for Raindrop.io User objects.

Includes the authenticated user profile, public user profiles,
user statistics, and connected service references.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserFiles(BaseModel):
    """File storage usage info."""

    model_config = ConfigDict(extra="ignore")

    used: int = 0
    size: int = 0
    last_checkout: datetime | None = Field(default=None, alias="lastCheckout")


class UserGroup(BaseModel):
    """A collection group (folder grouping in the sidebar)."""

    model_config = ConfigDict(extra="ignore")

    title: str = ""
    hidden: bool = False
    sort: int = 0
    collections: list[int] = Field(default_factory=list)


class User(BaseModel):
    """Authenticated user profile."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: int = Field(alias="_id", default=0)
    full_name: str = Field(default="", alias="fullName")
    email: str = ""
    avatar: str = ""
    pro: bool = False
    registered: datetime | None = None
    groups: list[UserGroup] = Field(default_factory=list)
    files: UserFiles | None = None
    last_action: datetime | None = Field(default=None, alias="lastAction")
    last_update: datetime | None = Field(default=None, alias="lastUpdate")
    last_visit: datetime | None = Field(default=None, alias="lastVisit")
    config: dict = Field(default_factory=dict)
    password: bool = False  # Whether user has a password set


class UserStats(BaseModel):
    """User account statistics."""

    model_config = ConfigDict(extra="ignore")

    items: int = 0
    trash: int = 0
    pro: bool = False


class UserUpdateRequest(BaseModel):
    """Request body for updating user profile."""

    model_config = ConfigDict(populate_by_name=True)

    full_name: str | None = Field(default=None, alias="fullName")
    password: str | None = None
    old_password: str | None = Field(default=None, alias="oldpassword")
    config: dict | None = None
    groups: list[dict] | None = None
    new_password: str | None = Field(default=None, alias="newpassword")

    def to_api_body(self) -> dict:
        """Convert to API request format."""
        return self.model_dump(exclude_none=True, by_alias=True)


class ConnectedService(BaseModel):
    """A connected third-party service (Google, Dropbox, etc.)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = ""
    connected: bool = False
