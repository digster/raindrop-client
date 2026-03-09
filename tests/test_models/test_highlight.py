"""Tests for Highlight models."""

from raindrop_client.models.highlight import Highlight, HighlightCreateRequest


class TestHighlight:
    def test_parse_api_response(self):
        data = {
            "_id": "abc123",
            "text": "Important quote",
            "note": "My note",
            "color": "yellow",
            "created": "2024-02-01T00:00:00.000Z",
            "lastUpdate": "2024-02-01T12:00:00.000Z",
        }
        h = Highlight.model_validate(data)
        assert h.id == "abc123"
        assert h.text == "Important quote"
        assert h.note == "My note"
        assert h.color == "yellow"
        assert h.last_update is not None

    def test_with_raindrop_ref(self):
        """Highlight includes raindrop ID when listed by collection."""
        h = Highlight.model_validate({"_id": "x", "text": "quote", "raindropRef": 99999})
        assert h.raindrop_id == 99999

    def test_minimal(self):
        h = Highlight.model_validate({"_id": "x", "text": "quote"})
        assert h.text == "quote"
        assert h.note == ""


class TestHighlightCreateRequest:
    def test_create(self):
        req = HighlightCreateRequest(text="Some text", color="red", note="Note")
        assert req.text == "Some text"
        assert req.color == "red"
        assert req.note == "Note"

    def test_defaults(self):
        req = HighlightCreateRequest(text="Text only")
        assert req.color == ""
        assert req.note == ""
