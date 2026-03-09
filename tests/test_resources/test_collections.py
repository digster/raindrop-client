"""Tests for the Collections resource."""

import httpx
import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.collections import CollectionsResource

from tests.conftest import make_collection

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestCollectionsResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return CollectionsResource(transport), transport

    def test_list_root(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/collections").respond(200, json={
                "result": True,
                "items": [make_collection(_id=1, title="Col1"), make_collection(_id=2, title="Col2")],
            })
            resource, transport = self._make_resource()
            result = resource.list_root()
            assert len(result) == 2
            assert result[0].id == 1
            assert result[1].title == "Col2"
            transport.close()

    def test_list_children(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/childrens").respond(200, json={
                "result": True,
                "items": [make_collection(_id=10, title="Child")],
            })
            resource, transport = self._make_resource()
            result = resource.list_children()
            assert len(result) == 1
            assert result[0].id == 10
            transport.close()

    def test_get(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/collection/12345").respond(200, json={
                "result": True,
                "item": make_collection(_id=12345, title="Specific"),
            })
            resource, transport = self._make_resource()
            result = resource.get(12345)
            assert result.id == 12345
            assert result.title == "Specific"
            transport.close()

    def test_create_with_kwargs(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/collection").respond(200, json={
                "result": True,
                "item": make_collection(_id=999, title="New"),
            })
            resource, transport = self._make_resource()
            result = resource.create(title="New", view="grid")
            assert result.id == 999
            assert result.title == "New"
            transport.close()

    def test_update(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/collection/12345").respond(200, json={
                "result": True,
                "item": make_collection(_id=12345, title="Updated"),
            })
            resource, transport = self._make_resource()
            result = resource.update(12345, title="Updated")
            assert result.title == "Updated"
            transport.close()

    def test_delete(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/collection/12345").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.delete(12345)
            assert result is True
            transport.close()

    def test_empty_trash(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/collection/-99").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.empty_trash()
            assert result is True
            transport.close()

    def test_reorder(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/collections").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.reorder(sort="title")
            assert result is True
            transport.close()

    def test_delete_many(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/collections").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.delete_many([1, 2, 3])
            assert result is True
            transport.close()

    def test_merge(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/collections/merge").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.merge([1, 2], to=3)
            assert result is True
            transport.close()
