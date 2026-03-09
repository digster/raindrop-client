"""Pydantic models for Raindrop.io Filter (facet count) objects.

Filters provide aggregated counts by tag, type, broken links, etc.
for a given collection — useful for building sidebar facet UIs.
"""

from pydantic import BaseModel, ConfigDict, Field


class FilterTagItem(BaseModel):
    """A tag facet with count."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    tag: str = Field(alias="_id", default="")
    count: int = 0


class FilterTypeItem(BaseModel):
    """A content type facet with count."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: str = Field(alias="_id", default="")
    count: int = 0


class FilterCountItem(BaseModel):
    """A simple count container (broken, duplicates, important, notag)."""

    model_config = ConfigDict(extra="ignore")

    count: int = 0


class FilterCounts(BaseModel):
    """Complete filter counts for a collection."""

    model_config = ConfigDict(extra="ignore")

    broken: FilterCountItem = Field(default_factory=FilterCountItem)
    duplicates: FilterCountItem = Field(default_factory=FilterCountItem)
    important: FilterCountItem = Field(default_factory=FilterCountItem)
    notag: FilterCountItem = Field(default_factory=FilterCountItem)
    tags: list[FilterTagItem] = Field(default_factory=list)
    types: list[FilterTypeItem] = Field(default_factory=list)
