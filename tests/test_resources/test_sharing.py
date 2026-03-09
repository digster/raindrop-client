"""Tests for the Sharing resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.sharing import SharingResource

from tests.conftest import make_collaborator

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestSharingResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return SharingResource(transport), transport

    def test_get_collaborators(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/collection/12345/sharing").respond(200, json={
                "result": True,
                "items": [make_collaborator(), make_collaborator(_id=2002, fullName="Another User")],
            })
            resource, transport = self._make_resource()
            result = resource.get_collaborators(12345)
            assert len(result) == 2
            assert result[0].id == 2001
            assert result[1].full_name == "Another User"
            transport.close()

    def test_share(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/collection/12345/sharing").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.share(12345, role="viewer", emails=["user@example.com"])
            assert result is True
            transport.close()

    def test_update_access(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/collection/12345/sharing/2001").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.update_access(12345, 2001, role="member")
            assert result is True
            transport.close()

    def test_remove_collaborator(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/collection/12345/sharing/2001").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.remove_collaborator(12345, 2001)
            assert result is True
            transport.close()

    def test_unshare(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/collection/12345/sharing").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.unshare(12345)
            assert result is True
            transport.close()

    def test_accept(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/collection/sharing/invite-token-123").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.accept("invite-token-123")
            assert result is True
            transport.close()
