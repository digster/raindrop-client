"""Tests for Filter models."""

from raindrop_client.models.filter import FilterCountItem, FilterCounts, FilterTagItem, FilterTypeItem


class TestFilterCounts:
    def test_parse_full_response(self):
        """FilterCounts parses complete API response."""
        data = {
            "result": True,
            "broken": {"count": 5},
            "duplicates": {"count": 3},
            "important": {"count": 20},
            "notag": {"count": 100},
            "tags": [
                {"_id": "python", "count": 42},
                {"_id": "api", "count": 15},
            ],
            "types": [
                {"_id": "article", "count": 200},
                {"_id": "image", "count": 50},
            ],
        }
        fc = FilterCounts.model_validate(data)
        assert fc.broken.count == 5
        assert fc.duplicates.count == 3
        assert fc.important.count == 20
        assert fc.notag.count == 100
        assert len(fc.tags) == 2
        assert fc.tags[0].tag == "python"
        assert fc.tags[0].count == 42
        assert len(fc.types) == 2
        assert fc.types[0].type == "article"

    def test_defaults(self):
        fc = FilterCounts()
        assert fc.broken.count == 0
        assert fc.tags == []
        assert fc.types == []


class TestFilterTagItem:
    def test_parse(self):
        item = FilterTagItem.model_validate({"_id": "javascript", "count": 30})
        assert item.tag == "javascript"
        assert item.count == 30


class TestFilterTypeItem:
    def test_parse(self):
        item = FilterTypeItem.model_validate({"_id": "video", "count": 10})
        assert item.type == "video"
        assert item.count == 10
