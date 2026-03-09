"""Tests for shared model types."""

from raindrop_client.models.common import (
    AccessLevel,
    CollectionRef,
    Creator,
    MediaItem,
    RaindropType,
    UserRef,
    View,
)


class TestCollectionRef:
    def test_parse_dollar_id(self):
        """CollectionRef parses Raindrop's $id format."""
        ref = CollectionRef.model_validate({"$id": 12345})
        assert ref.id == 12345

    def test_extra_fields_ignored(self):
        """Unknown fields don't break parsing."""
        ref = CollectionRef.model_validate({"$id": 1, "extra": "ignored"})
        assert ref.id == 1


class TestAccessLevel:
    def test_defaults(self):
        level = AccessLevel()
        assert level.level == 0
        assert level.draggable is True

    def test_from_api(self):
        level = AccessLevel.model_validate({"level": 4, "draggable": False})
        assert level.level == 4
        assert level.draggable is False


class TestView:
    def test_enum_values(self):
        assert View.LIST == "list"
        assert View.GRID == "grid"
        assert View.MASONRY == "masonry"


class TestRaindropType:
    def test_enum_values(self):
        assert RaindropType.LINK == "link"
        assert RaindropType.ARTICLE == "article"
        assert RaindropType.IMAGE == "image"
        assert RaindropType.VIDEO == "video"
        assert RaindropType.DOCUMENT == "document"


class TestMediaItem:
    def test_from_api(self):
        item = MediaItem.model_validate({"link": "https://img.com/x.jpg", "type": "image"})
        assert item.link == "https://img.com/x.jpg"
        assert item.type == "image"


class TestCreator:
    def test_from_api(self):
        creator = Creator.model_validate({"_id": 1001, "fullName": "Alice", "avatar": "https://img.com/a.jpg"})
        assert creator.id == 1001
        assert creator.full_name == "Alice"


class TestUserRef:
    def test_from_api(self):
        ref = UserRef.model_validate({"$id": 999})
        assert ref.id == 999
