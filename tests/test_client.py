"""Tests for the RaindropClient facade."""

import os
import pytest

from raindrop_client.client import RaindropClient
from raindrop_client.exceptions import AuthenticationError
from raindrop_client.resources.collections import CollectionsResource
from raindrop_client.resources.raindrops import RaindropsResource
from raindrop_client.resources.tags import TagsResource
from raindrop_client.resources.user import UserResource
from raindrop_client.resources.highlights import HighlightsResource
from raindrop_client.resources.filters import FiltersResource
from raindrop_client.resources.sharing import SharingResource
from raindrop_client.resources.import_export import ImportExportResource
from raindrop_client.resources.backups import BackupsResource


class TestRaindropClient:
    """Tests for client initialization and resource group setup."""

    def test_init_with_token(self):
        """Client initializes with explicit token."""
        client = RaindropClient(token="test-token")
        assert client._transport._token == "test-token"
        client.close()

    def test_init_from_env(self, monkeypatch):
        """Client reads token from RAINDROP_TEST_TOKEN env var."""
        monkeypatch.setenv("RAINDROP_TEST_TOKEN", "env-token-123")
        client = RaindropClient()
        assert client._transport._token == "env-token-123"
        client.close()

    def test_init_no_token_raises(self, monkeypatch):
        """Client raises AuthenticationError when no token is available."""
        monkeypatch.delenv("RAINDROP_TEST_TOKEN", raising=False)
        with pytest.raises(AuthenticationError, match="No API token"):
            RaindropClient()

    def test_resource_groups_initialized(self):
        """All resource groups are initialized as correct types."""
        client = RaindropClient(token="test-token")

        assert isinstance(client.collections, CollectionsResource)
        assert isinstance(client.raindrops, RaindropsResource)
        assert isinstance(client.tags, TagsResource)
        assert isinstance(client.user, UserResource)
        assert isinstance(client.highlights, HighlightsResource)
        assert isinstance(client.filters, FiltersResource)
        assert isinstance(client.sharing, SharingResource)
        assert isinstance(client.import_export, ImportExportResource)
        assert isinstance(client.backups, BackupsResource)

        client.close()

    def test_context_manager(self):
        """Client works as a context manager."""
        with RaindropClient(token="test-token") as client:
            assert client is not None

    def test_repr(self):
        """Client repr shows base URL."""
        client = RaindropClient(token="test-token")
        assert "api.raindrop.io" in repr(client)
        client.close()

    def test_explicit_token_overrides_env(self, monkeypatch):
        """Explicit token parameter takes priority over env var."""
        monkeypatch.setenv("RAINDROP_TEST_TOKEN", "env-token")
        client = RaindropClient(token="explicit-token")
        assert client._transport._token == "explicit-token"
        client.close()
