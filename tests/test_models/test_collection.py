"""Tests for Collection models."""

from raindrop_client.models.collection import Collection, CollectionCreateRequest, CollectionUpdateRequest


class TestCollection:
    def test_parse_api_response(self):
        """Collection parses full API response correctly."""
        data = {
            "_id": 12345,
            "title": "My Collection",
            "description": "A test collection",
            "color": "#ff0000",
            "cover": ["https://img.com/cover.jpg"],
            "count": 42,
            "view": "grid",
            "public": True,
            "expanded": False,
            "sort": 5,
            "parent": {"$id": 100},
            "user": {"$id": 1001},
            "access": {"level": 4, "draggable": True},
            "created": "2024-01-01T00:00:00.000Z",
            "lastUpdate": "2024-06-15T10:30:00.000Z",
            "slug": "my-collection",
        }
        col = Collection.model_validate(data)
        assert col.id == 12345
        assert col.title == "My Collection"
        assert col.count == 42
        assert col.view == "grid"
        assert col.public is True
        assert col.parent.id == 100
        assert col.user.id == 1001
        assert col.last_update is not None

    def test_minimal_collection(self):
        """Collection works with minimal data."""
        col = Collection.model_validate({"_id": 1, "title": "Min"})
        assert col.id == 1
        assert col.title == "Min"
        assert col.count == 0
        assert col.parent is None

    def test_extra_fields_ignored(self):
        """Unknown API fields don't break parsing."""
        col = Collection.model_validate({"_id": 1, "title": "X", "future_field": "value"})
        assert col.id == 1


class TestCollectionCreateRequest:
    def test_to_api_body(self):
        """Creates correct API body with parent.$id."""
        req = CollectionCreateRequest(title="New", view="grid", parent_id=100)
        body = req.to_api_body()
        assert body["title"] == "New"
        assert body["view"] == "grid"
        assert body["parent"] == {"$id": 100}
        assert "parent_id" not in body

    def test_without_parent(self):
        """Root collection omits parent."""
        req = CollectionCreateRequest(title="Root")
        body = req.to_api_body()
        assert body == {"title": "Root"}

    def test_excludes_none_fields(self):
        """None optional fields are excluded from body."""
        req = CollectionCreateRequest(title="X")
        body = req.to_api_body()
        assert "view" not in body
        assert "public" not in body


class TestCollectionUpdateRequest:
    def test_to_api_body_partial(self):
        """Update only includes provided fields."""
        req = CollectionUpdateRequest(title="Updated Title")
        body = req.to_api_body()
        assert body == {"title": "Updated Title"}

    def test_to_api_body_with_parent(self):
        """Update handles parent.$id correctly."""
        req = CollectionUpdateRequest(parent_id=200)
        body = req.to_api_body()
        assert body["parent"] == {"$id": 200}
