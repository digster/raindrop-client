"""Tests for the Raindrops resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.raindrops import RaindropsResource

from tests.conftest import make_raindrop

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestRaindropsResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return RaindropsResource(transport), transport

    def test_get(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrop/99999").respond(200, json={
                "result": True,
                "item": make_raindrop(_id=99999),
            })
            resource, transport = self._make_resource()
            result = resource.get(99999)
            assert result.id == 99999
            assert result.link == "https://example.com"
            transport.close()

    def test_create_with_kwargs(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/raindrop").respond(200, json={
                "result": True,
                "item": make_raindrop(_id=100, link="https://new.com", tags=["ai"]),
            })
            resource, transport = self._make_resource()
            result = resource.create(link="https://new.com", tags=["ai"])
            assert result.id == 100
            assert result.tags == ["ai"]
            transport.close()

    def test_update(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/raindrop/99999").respond(200, json={
                "result": True,
                "item": make_raindrop(_id=99999, title="Updated"),
            })
            resource, transport = self._make_resource()
            result = resource.update(99999, title="Updated")
            assert result.title == "Updated"
            transport.close()

    def test_delete(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/raindrop/99999").respond(200, json={"result": True})
            resource, transport = self._make_resource()
            result = resource.delete(99999)
            assert result is True
            transport.close()

    def test_list_with_params(self):
        with respx.mock(base_url=BASE) as router:
            route = router.get("/raindrops/0").respond(200, json={
                "result": True,
                "items": [make_raindrop(_id=1), make_raindrop(_id=2)],
            })
            resource, transport = self._make_resource()
            result = resource.list(collection_id=0, search="python", sort="-created", page=1, perpage=10)
            assert len(result) == 2

            # Verify query params were sent
            request = route.calls[0].request
            assert "search=python" in str(request.url)
            assert "page=1" in str(request.url)
            transport.close()

    def test_list_default_params(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrops/0").respond(200, json={
                "result": True,
                "items": [],
            })
            resource, transport = self._make_resource()
            result = resource.list()
            assert result == []
            transport.close()

    def test_create_many(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/raindrops").respond(200, json={
                "result": True,
                "items": [make_raindrop(_id=1), make_raindrop(_id=2)],
            })
            resource, transport = self._make_resource()
            result = resource.create_many([
                {"link": "https://a.com"},
                {"link": "https://b.com"},
            ])
            assert len(result) == 2
            transport.close()

    def test_update_many(self):
        with respx.mock(base_url=BASE) as router:
            router.put("/raindrops/0").respond(200, json={"result": True, "modified": 5})
            resource, transport = self._make_resource()
            result = resource.update_many(ids=[1, 2, 3], important=True)
            assert result["modified"] == 5
            transport.close()

    def test_delete_many(self):
        with respx.mock(base_url=BASE) as router:
            router.delete("/raindrops/-99").respond(200, json={"result": True, "modified": 10})
            resource, transport = self._make_resource()
            result = resource.delete_many(collection_id=-99, ids=[1, 2])
            assert result["modified"] == 10
            transport.close()

    def test_suggest_for_url(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/raindrop/suggest").respond(200, json={
                "result": True,
                "item": {
                    "collections": [{"$id": 100}, {"$id": 200}],
                    "tags": ["python", "dev"],
                },
            })
            resource, transport = self._make_resource()
            result = resource.suggest_for_url("https://example.com")
            assert len(result.collections) == 2
            assert result.tags == ["python", "dev"]
            transport.close()

    def test_suggest_for_existing(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrop/99999/suggest").respond(200, json={
                "result": True,
                "item": {
                    "collections": [{"$id": 300}],
                    "tags": ["ai"],
                },
            })
            resource, transport = self._make_resource()
            result = resource.suggest_for_existing(99999)
            assert result.collections[0].id == 300
            transport.close()

    def test_get_cache(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrop/99999/cache").respond(200, content=b"<html>cached page</html>")
            resource, transport = self._make_resource()
            result = resource.get_cache(99999)
            assert b"cached page" in result
            transport.close()
