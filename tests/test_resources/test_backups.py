"""Tests for the Backups resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.backups import BackupsResource

from tests.conftest import make_backup

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestBackupsResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return BackupsResource(transport), transport

    def test_list(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/backups").respond(200, json={
                "result": True,
                "items": [make_backup(), make_backup(_id="backup-002")],
            })
            resource, transport = self._make_resource()
            result = resource.list()
            assert len(result) == 2
            assert result[0].id == "backup-001"
            assert result[1].id == "backup-002"
            transport.close()

    def test_generate(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/backup").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.generate()
            assert result is True
            transport.close()

    def test_download(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/backup/backup-001").respond(200, content=b"backup file content")
            resource, transport = self._make_resource()
            result = resource.download("backup-001")
            assert result == b"backup file content"
            transport.close()
