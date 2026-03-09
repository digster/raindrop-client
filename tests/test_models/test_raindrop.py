"""Tests for Raindrop models."""

from raindrop_client.models.raindrop import (
    CacheStatus,
    Raindrop,
    RaindropCache,
    RaindropCreateRequest,
    RaindropFile,
    RaindropSuggestion,
    RaindropUpdateRequest,
)


class TestRaindrop:
    def test_parse_full_response(self):
        """Raindrop parses complete API response."""
        data = {
            "_id": 99999,
            "link": "https://example.com/article",
            "title": "Great Article",
            "excerpt": "A summary",
            "note": "My notes",
            "type": "article",
            "cover": "https://example.com/cover.jpg",
            "tags": ["python", "api"],
            "important": True,
            "removed": False,
            "domain": "example.com",
            "collection": {"$id": 12345},
            "creator": {"_id": 1001, "fullName": "User", "avatar": ""},
            "media": [{"link": "https://img.com/1.jpg", "type": "image"}],
            "highlights": [{"text": "quote", "color": "yellow"}],
            "created": "2024-01-10T00:00:00.000Z",
            "lastUpdate": "2024-01-10T12:00:00.000Z",
            "order": 5,
        }
        rd = Raindrop.model_validate(data)
        assert rd.id == 99999
        assert rd.link == "https://example.com/article"
        assert rd.title == "Great Article"
        assert rd.type == "article"
        assert rd.tags == ["python", "api"]
        assert rd.important is True
        assert rd.collection.id == 12345
        assert rd.creator.id == 1001
        assert len(rd.media) == 1
        assert rd.last_update is not None

    def test_minimal_raindrop(self):
        """Raindrop works with minimal data."""
        rd = Raindrop.model_validate({"_id": 1, "link": "https://x.com"})
        assert rd.id == 1
        assert rd.tags == []
        assert rd.collection is None

    def test_cache_info(self):
        """RaindropCache parses status."""
        cache = RaindropCache.model_validate({"status": "ready", "size": 12345})
        assert cache.status == "ready"
        assert cache.size == 12345

    def test_file_info(self):
        """RaindropFile parses file metadata."""
        f = RaindropFile.model_validate({"name": "doc.pdf", "size": 5000, "type": "application/pdf"})
        assert f.name == "doc.pdf"
        assert f.size == 5000


class TestRaindropCreateRequest:
    def test_to_api_body_with_collection(self):
        """Creates API body with collection.$id."""
        req = RaindropCreateRequest(
            link="https://example.com",
            title="Example",
            tags=["test"],
            collection_id=12345,
        )
        body = req.to_api_body()
        assert body["link"] == "https://example.com"
        assert body["title"] == "Example"
        assert body["tags"] == ["test"]
        assert body["collection"] == {"$id": 12345}
        assert "collection_id" not in body

    def test_please_parse(self):
        """pleaseParse is included as empty dict when True."""
        req = RaindropCreateRequest(link="https://example.com", please_parse=True)
        body = req.to_api_body()
        assert body["pleaseParse"] == {}

    def test_minimal_body(self):
        """Only link is required."""
        req = RaindropCreateRequest(link="https://example.com")
        body = req.to_api_body()
        assert body == {"link": "https://example.com"}


class TestRaindropUpdateRequest:
    def test_partial_update(self):
        """Update only includes changed fields."""
        req = RaindropUpdateRequest(title="New Title", tags=["updated"])
        body = req.to_api_body()
        assert body == {"title": "New Title", "tags": ["updated"]}

    def test_move_to_collection(self):
        """Moving to a different collection uses $id format."""
        req = RaindropUpdateRequest(collection_id=999)
        body = req.to_api_body()
        assert body["collection"] == {"$id": 999}


class TestRaindropSuggestion:
    def test_parse_suggestion(self):
        """Suggestion parses collections and tags."""
        data = {
            "collections": [{"$id": 100}, {"$id": 200}],
            "tags": ["python", "api"],
        }
        suggestion = RaindropSuggestion.model_validate(data)
        assert len(suggestion.collections) == 2
        assert suggestion.collections[0].id == 100
        assert suggestion.tags == ["python", "api"]


class TestCacheStatus:
    def test_enum_values(self):
        assert CacheStatus.READY == "ready"
        assert CacheStatus.RETRY == "retry"
        assert CacheStatus.FAILED == "failed"
