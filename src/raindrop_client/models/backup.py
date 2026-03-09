"""Pydantic models for Raindrop.io Backup objects.

Backups are snapshots of user data that can be downloaded in various formats.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Backup(BaseModel):
    """A backup snapshot record."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    id: str = Field(alias="_id", default="")
    created: datetime | None = None
