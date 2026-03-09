"""Main client facade for the Raindrop.io API.

RaindropClient is the single entry point — it initializes the HTTP transport
and exposes all resource groups as attributes for a clean, discoverable API:

    client = RaindropClient(token="...")
    client.collections.list_root()
    client.raindrops.create(link="https://example.com", tags=["ai"])
    client.tags.list()
    client.user.get()
"""

import os

from dotenv import load_dotenv

from raindrop_client.config import API_BASE_URL, DEFAULT_TIMEOUT, ENV_TEST_TOKEN
from raindrop_client.exceptions import AuthenticationError
from raindrop_client.http import HttpTransport
from raindrop_client.resources.backups import BackupsResource
from raindrop_client.resources.collections import CollectionsResource
from raindrop_client.resources.filters import FiltersResource
from raindrop_client.resources.highlights import HighlightsResource
from raindrop_client.resources.import_export import ImportExportResource
from raindrop_client.resources.raindrops import RaindropsResource
from raindrop_client.resources.sharing import SharingResource
from raindrop_client.resources.tags import TagsResource
from raindrop_client.resources.user import UserResource


class RaindropClient:
    """Raindrop.io API client with resource-grouped methods.

    Authenticates using either a directly provided token or the
    RAINDROP_TEST_TOKEN environment variable.

    Args:
        token: API access token (test token or OAuth2 access token).
        base_url: API base URL (default: https://api.raindrop.io).
        timeout: Request timeout in seconds.

    Raises:
        AuthenticationError: If no token is provided or found in env vars.
    """

    def __init__(
        self,
        token: str | None = None,
        base_url: str = API_BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
    ):
        # Load .env file if present
        load_dotenv()

        # Resolve token: explicit param > env var
        resolved_token = token or os.environ.get(ENV_TEST_TOKEN)
        if not resolved_token:
            raise AuthenticationError(
                f"No API token provided. Pass token= or set {ENV_TEST_TOKEN} environment variable."
            )

        self._transport = HttpTransport(token=resolved_token, base_url=base_url, timeout=timeout)

        # Initialize resource groups
        self.collections = CollectionsResource(self._transport)
        self.raindrops = RaindropsResource(self._transport)
        self.tags = TagsResource(self._transport)
        self.user = UserResource(self._transport)
        self.highlights = HighlightsResource(self._transport)
        self.filters = FiltersResource(self._transport)
        self.sharing = SharingResource(self._transport)
        self.import_export = ImportExportResource(self._transport)
        self.backups = BackupsResource(self._transport)

    def close(self) -> None:
        """Close the underlying HTTP transport."""
        self._transport.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self) -> str:
        return f"RaindropClient(base_url={self._transport._base_url!r})"
