"""Tests for Sharing models."""

from raindrop_client.models.sharing import Collaborator, ShareInviteRequest


class TestCollaborator:
    def test_parse_api_response(self):
        data = {
            "_id": 2001,
            "email": "collab@example.com",
            "email_MD5": "abc123",
            "fullName": "Collaborator",
            "registered": "2021-06-15T00:00:00.000Z",
            "role": "viewer",
        }
        collab = Collaborator.model_validate(data)
        assert collab.id == 2001
        assert collab.email == "collab@example.com"
        assert collab.email_md5 == "abc123"
        assert collab.full_name == "Collaborator"
        assert collab.role == "viewer"


class TestShareInviteRequest:
    def test_create(self):
        req = ShareInviteRequest(role="member", emails=["user@example.com"])
        assert req.role == "member"
        assert req.emails == ["user@example.com"]

    def test_defaults(self):
        req = ShareInviteRequest()
        assert req.role == "viewer"
        assert req.emails == []
