"""Tests for User models."""

from raindrop_client.models.user import ConnectedService, User, UserStats, UserUpdateRequest


class TestUser:
    def test_parse_api_response(self):
        """User parses full API response."""
        data = {
            "_id": 1001,
            "fullName": "Alice Smith",
            "email": "alice@example.com",
            "avatar": "https://img.com/avatar.jpg",
            "pro": True,
            "registered": "2020-01-01T00:00:00.000Z",
            "groups": [{"title": "Dev", "hidden": False, "sort": 0, "collections": [1, 2, 3]}],
            "files": {"used": 50, "size": 1000000},
            "config": {"lang": "en"},
            "password": True,
        }
        user = User.model_validate(data)
        assert user.id == 1001
        assert user.full_name == "Alice Smith"
        assert user.email == "alice@example.com"
        assert user.pro is True
        assert len(user.groups) == 1
        assert user.groups[0].title == "Dev"
        assert user.groups[0].collections == [1, 2, 3]

    def test_minimal_user(self):
        user = User.model_validate({"_id": 1})
        assert user.id == 1
        assert user.full_name == ""
        assert user.groups == []


class TestUserStats:
    def test_parse_stats(self):
        stats = UserStats.model_validate({"items": 500, "trash": 10, "pro": True})
        assert stats.items == 500
        assert stats.trash == 10
        assert stats.pro is True


class TestUserUpdateRequest:
    def test_to_api_body(self):
        req = UserUpdateRequest(full_name="New Name")
        body = req.to_api_body()
        assert body["fullName"] == "New Name"

    def test_excludes_none(self):
        req = UserUpdateRequest(full_name="Name")
        body = req.to_api_body()
        assert "password" not in body
        assert "config" not in body


class TestConnectedService:
    def test_parse(self):
        svc = ConnectedService.model_validate({"name": "google", "connected": True})
        assert svc.name == "google"
        assert svc.connected is True
