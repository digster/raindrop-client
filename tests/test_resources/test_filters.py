"""Tests for the Filters resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.filters import FiltersResource

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestFiltersResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return FiltersResource(transport), transport

    def test_get_filters(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/filters/0").respond(200, json={
                "result": True,
                "broken": {"count": 5},
                "duplicates": {"count": 3},
                "important": {"count": 20},
                "notag": {"count": 100},
                "tags": [{"_id": "python", "count": 42}],
                "types": [{"_id": "article", "count": 200}],
            })
            resource, transport = self._make_resource()
            result = resource.get(0)
            assert result.broken.count == 5
            assert result.notag.count == 100
            assert len(result.tags) == 1
            assert result.tags[0].tag == "python"
            transport.close()

    def test_get_with_params(self):
        with respx.mock(base_url=BASE) as router:
            route = router.get("/filters/12345").respond(200, json={
                "result": True,
                "broken": {"count": 0},
                "duplicates": {"count": 0},
                "important": {"count": 0},
                "notag": {"count": 0},
                "tags": [],
                "types": [],
            })
            resource, transport = self._make_resource()
            resource.get(12345, tags_sort="_id", search="python")

            request = route.calls[0].request
            assert "tagsSort=_id" in str(request.url)
            assert "search=python" in str(request.url)
            transport.close()
