"""Tests for Tag models."""

from raindrop_client.models.tag import Tag, TagDeleteRequest, TagMergeRequest, TagRenameRequest


class TestTag:
    def test_parse_api_response(self):
        """Tag parses _id as tag name."""
        tag = Tag.model_validate({"_id": "python", "count": 42})
        assert tag.tag == "python"
        assert tag.count == 42

    def test_defaults(self):
        """Tag has sensible defaults."""
        tag = Tag()
        assert tag.tag == ""
        assert tag.count == 0


class TestTagRenameRequest:
    def test_rename(self):
        req = TagRenameRequest(tags=["old-tag"], replace="new-tag")
        assert req.tags == ["old-tag"]
        assert req.replace == "new-tag"


class TestTagMergeRequest:
    def test_merge(self):
        req = TagMergeRequest(tags=["tag1", "tag2"], replace="merged-tag")
        assert len(req.tags) == 2
        assert req.replace == "merged-tag"


class TestTagDeleteRequest:
    def test_delete(self):
        req = TagDeleteRequest(tags=["unwanted-tag"])
        assert req.tags == ["unwanted-tag"]
