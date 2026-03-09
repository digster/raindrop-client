"""Tests for the Tags resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.tags import TagsResource

from tests.conftest import make_tag

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestTagsResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return TagsResource(transport), transport

    def test_list_all(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/tags").respond(200, json={
                "result": True,
                "items": [make_tag(_id="python", count=42), make_tag(_id="api", count=15)],
            })
            resource, transport = self._make_resource()
            result = resource.list()
            assert len(result) == 2
            assert result[0].tag == "python"
            assert result[0].count == 42
            transport.close()

    def test_list_by_collection(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/tags/12345").respond(200, json={
                "result": True,
                "items": [make_tag(_id="specific", count=5)],
            })
            resource, transport = self._make_resource()
            result = resource.list(collection_id=12345)
            assert len(result) == 1
            assert result[0].tag == "specific"
            transport.close()

    def test_rename(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/tags").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.rename(tags=["old-name"], replace="new-name")
            assert result is True
            transport.close()

    def test_rename_in_collection(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/tags/12345").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.rename(tags=["old"], replace="new", collection_id=12345)
            assert result is True
            transport.close()

    def test_merge(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/tags").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.merge(tags=["tag1", "tag2"], replace="merged")
            assert result is True
            transport.close()

    def test_delete(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/tags").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.delete(tags=["unwanted"])
            assert result is True
            transport.close()

    def test_delete_in_collection(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/tags/12345").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.delete(tags=["old"], collection_id=12345)
            assert result is True
            transport.close()
