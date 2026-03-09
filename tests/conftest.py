"""Shared test fixtures and factories for the Raindrop.io client test suite."""

import httpx
import pytest
import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport


@pytest.fixture
def base_url():
    """Base URL for the API."""
    return API_BASE_URL


@pytest.fixture
def api_url(base_url):
    """Full API URL prefix."""
    return f"{base_url}{API_PREFIX}"


@pytest.fixture
def mock_transport(base_url):
    """HttpTransport with a mocked httpx client."""
    transport = HttpTransport(token="test-token-123", base_url=base_url)
    return transport


@pytest.fixture
def respx_mock():
    """Pre-configured respx mock router."""
    with respx.mock(base_url=f"{API_BASE_URL}{API_PREFIX}") as router:
        yield router


# -- Factory functions for creating test data --

def make_collection(**overrides) -> dict:
    """Create a collection API response dict."""
    data = {
        "_id": 12345,
        "title": "Test Collection",
        "description": "",
        "color": "",
        "cover": [],
        "count": 10,
        "view": "list",
        "public": False,
        "expanded": True,
        "sort": 0,
        "parent": None,
        "user": {"$id": 1001},
        "access": {"level": 4, "draggable": True},
        "created": "2024-01-01T00:00:00.000Z",
        "lastUpdate": "2024-01-15T00:00:00.000Z",
        "slug": "test-collection",
    }
    data.update(overrides)
    return data


def make_raindrop(**overrides) -> dict:
    """Create a raindrop API response dict."""
    data = {
        "_id": 99999,
        "link": "https://example.com",
        "title": "Example Page",
        "excerpt": "An example page",
        "note": "",
        "type": "link",
        "cover": "https://example.com/cover.jpg",
        "tags": ["test", "example"],
        "important": False,
        "removed": False,
        "domain": "example.com",
        "collection": {"$id": 12345},
        "creator": {"_id": 1001, "fullName": "Test User", "avatar": ""},
        "media": [],
        "highlights": [],
        "created": "2024-01-10T00:00:00.000Z",
        "lastUpdate": "2024-01-10T12:00:00.000Z",
        "order": 0,
    }
    data.update(overrides)
    return data


def make_tag(**overrides) -> dict:
    """Create a tag API response dict."""
    data = {
        "_id": "python",
        "count": 42,
    }
    data.update(overrides)
    return data


def make_user(**overrides) -> dict:
    """Create a user API response dict."""
    data = {
        "_id": 1001,
        "fullName": "Test User",
        "email": "test@example.com",
        "avatar": "https://example.com/avatar.jpg",
        "pro": True,
        "registered": "2020-01-01T00:00:00.000Z",
        "groups": [],
        "files": {"used": 100, "size": 1000000},
        "config": {},
        "password": True,
    }
    data.update(overrides)
    return data


def make_highlight(**overrides) -> dict:
    """Create a highlight API response dict."""
    data = {
        "_id": "abc123",
        "text": "Important quote from article",
        "note": "This is key",
        "color": "yellow",
        "created": "2024-02-01T00:00:00.000Z",
        "lastUpdate": "2024-02-01T12:00:00.000Z",
    }
    data.update(overrides)
    return data


def make_collaborator(**overrides) -> dict:
    """Create a collaborator API response dict."""
    data = {
        "_id": 2001,
        "email": "collab@example.com",
        "email_MD5": "abc123def456",
        "fullName": "Collaborator User",
        "registered": "2021-06-15T00:00:00.000Z",
        "role": "viewer",
    }
    data.update(overrides)
    return data


def make_backup(**overrides) -> dict:
    """Create a backup API response dict."""
    data = {
        "_id": "backup-001",
        "created": "2024-03-01T00:00:00.000Z",
    }
    data.update(overrides)
    return data
