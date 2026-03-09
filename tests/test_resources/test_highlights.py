"""Tests for the Highlights resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.highlights import HighlightsResource

from tests.conftest import make_highlight, make_raindrop

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestHighlightsResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return HighlightsResource(transport), transport

    def test_list_for_raindrop(self):
        with respx.mock(base_url=BASE) as router:
            raindrop_data = make_raindrop(highlights=[
                make_highlight(_id="h1", text="Quote 1"),
                make_highlight(_id="h2", text="Quote 2"),
            ])
            router.get("/raindrop/99999").respond(200, json={
                "result": True,
                "item": raindrop_data,
            })
            resource, transport = self._make_resource()
            result = resource.list(99999)
            assert len(result) == 2
            assert result[0].id == "h1"
            assert result[1].text == "Quote 2"
            transport.close()

    def test_list_by_collection(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/highlights/0").respond(200, json={
                "result": True,
                "items": [
                    make_highlight(_id="h1", text="Quote 1", raindropRef=100),
                    make_highlight(_id="h2", text="Quote 2", raindropRef=200),
                ],
            })
            resource, transport = self._make_resource()
            result = resource.list_by_collection(0)
            assert len(result) == 2
            assert result[0].raindrop_id == 100
            transport.close()

    def test_list_empty(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrop/99999").respond(200, json={
                "result": True,
                "item": make_raindrop(highlights=[]),
            })
            resource, transport = self._make_resource()
            result = resource.list(99999)
            assert result == []
            transport.close()
