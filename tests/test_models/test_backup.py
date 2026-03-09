"""Tests for Backup models."""

from raindrop_client.models.backup import Backup


class TestBackup:
    def test_parse_api_response(self):
        data = {
            "_id": "backup-001",
            "created": "2024-03-01T00:00:00.000Z",
        }
        backup = Backup.model_validate(data)
        assert backup.id == "backup-001"
        assert backup.created is not None

    def test_extra_fields(self):
        backup = Backup.model_validate({"_id": "b1", "extra": "ignored"})
        assert backup.id == "b1"
