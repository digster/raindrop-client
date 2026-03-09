"""Resource class for Raindrop.io Import/Export endpoints.

Handles URL checking, bookmark file import (HTML/Netscape), and
collection export (CSV/HTML/ZIP).
"""

from raindrop_client.http import HttpTransport


class ImportExportResource:
    """Manages import and export operations."""

    def __init__(self, transport: HttpTransport):
        self._transport = transport

    def parse_url(self, link: str) -> dict:
        """Parse a URL and extract its metadata (title, description, etc.).

        Args:
            link: The URL to parse.

        Returns:
            Dict with extracted metadata (title, excerpt, media, etc.).
        """
        data = self._transport.get("/import/url/parse", params={"url": link})
        return data.get("item", {})

    def check_urls(self, urls: list[str]) -> list[dict]:
        """Check which URLs already exist as raindrops.

        Args:
            urls: List of URLs to check.

        Returns:
            List of match results with raindrop IDs for existing URLs.
        """
        data = self._transport.post("/import/url/exists", json_body={"urls": urls})
        return data.get("ids", [])

    def import_file(self, file_data: bytes, filename: str = "bookmarks.html") -> dict:
        """Import bookmarks from an HTML file (Netscape/Pocket/Instapaper format).

        Args:
            file_data: Raw bytes of the HTML bookmark file.
            filename: Name for the uploaded file.

        Returns:
            Dict with parsed bookmark structure.
        """
        return self._transport.upload_post(
            "/import/file",
            file_data=file_data,
            filename=filename,
            field_name="import",
            content_type="text/html",
        )

    def export(self, collection_id: int = 0, format: str = "csv", search: str | None = None, sort: str | None = None) -> bytes:
        """Export raindrops from a collection.

        Args:
            collection_id: Collection to export. 0 = all.
            format: Export format — "csv", "html", or "zip".
            search: Optional search query to filter exports.
            sort: Optional sort order.

        Returns:
            Raw bytes of the exported file.
        """
        params: dict = {}
        if search:
            params["search"] = search
        if sort:
            params["sort"] = sort

        return self._transport.download(
            f"/raindrops/{collection_id}/export.{format}",
            params=params if params else None,
        )
