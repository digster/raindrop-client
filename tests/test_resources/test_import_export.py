"""Tests for the ImportExport resource."""

import respx

from raindrop_client.config import API_BASE_URL, API_PREFIX
from raindrop_client.http import HttpTransport
from raindrop_client.resources.import_export import ImportExportResource

BASE = f"{API_BASE_URL}{API_PREFIX}"


class TestImportExportResource:
    def _make_resource(self):
        transport = HttpTransport(token="test-token")
        return ImportExportResource(transport), transport

    def test_parse_url(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/import/url/parse").respond(200, json={
                "result": True,
                "item": {
                    "title": "Example Page",
                    "excerpt": "A description",
                    "media": [{"link": "https://example.com/img.jpg"}],
                },
            })
            resource, transport = self._make_resource()
            result = resource.parse_url("https://example.com")
            assert result["title"] == "Example Page"
            transport.close()

    def test_check_urls(self):
        with respx.mock(base_url=BASE) as router:
            router.post("/import/url/exists").respond(200, json={
                "result": True,
                "ids": [99999],
            })
            resource, transport = self._make_resource()
            result = resource.check_urls(["https://example.com"])
            assert result == [99999]
            transport.close()

    def test_export_csv(self):
        with respx.mock(base_url=BASE) as router:
            router.get("/raindrops/0/export.csv").respond(200, content=b"title,link\nTest,https://example.com")
            resource, transport = self._make_resource()
            result = resource.export(collection_id=0, format="csv")
            assert b"title,link" in result
            transport.close()

    def test_export_with_params(self):
        with respx.mock(base_url=BASE) as router:
            route = router.get("/raindrops/12345/export.html").respond(200, content=b"<html>")
            resource, transport = self._make_resource()
            resource.export(collection_id=12345, format="html", search="python", sort="-created")

            request = route.calls[0].request
            assert "search=python" in str(request.url)
            assert "sort=-created" in str(request.url)
            transport.close()
