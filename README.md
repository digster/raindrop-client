# Raindrop.io Python API Client

A typed Python client library for the [Raindrop.io](https://raindrop.io) REST API v1. Designed for developers and LLMs — full type safety with Pydantic v2 models, resource-grouped methods, and built-in rate limiting/retry.

## Features

- **Full API coverage**: Collections, raindrops (bookmarks), tags, user, highlights, filters, sharing, import/export, and backups
- **Pydantic v2 models**: Type-safe request/response objects with auto-validation
- **Resource-grouped API**: Clean `client.resource.method()` interface
- **Rate limit handling**: Automatic retry with backoff on 429 responses
- **Typed exceptions**: Specific exception classes for each HTTP error type
- **OAuth2 + test token**: Supports both authentication methods
- **File uploads/downloads**: Multipart uploads and raw byte downloads for exports/backups

## Installation

```bash
# Using uv
uv add raindrop-client

# Or from source
git clone <repo-url>
cd raindrop-client
uv sync
```

## Quick Start

```python
from raindrop_client import RaindropClient

# Using a test token (from https://app.raindrop.io/settings/integrations)
client = RaindropClient(token="your-test-token")
# Or set RAINDROP_TEST_TOKEN env var and omit the token param

# Collections
collections = client.collections.list_root()
new_collection = client.collections.create(title="AI Papers")

# Bookmarks (raindrops)
bookmarks = client.raindrops.list(collection_id=0)  # 0 = all
bookmark = client.raindrops.create(
    link="https://example.com/article",
    title="Great Article",
    tags=["ai", "research"],
    collection_id=new_collection.id,
)

# Tags
tags = client.tags.list()
client.tags.rename(tags=["old-name"], replace="new-name")

# User
user = client.user.get()
print(f"Logged in as {user.full_name}")

# Search
results = client.raindrops.list(collection_id=0, search="python")

# Export
csv_data = client.import_export.export(collection_id=0, format="csv")
```

## Authentication

### Test Token (recommended for personal use)

1. Go to [Raindrop.io Integrations](https://app.raindrop.io/settings/integrations)
2. Create a test token
3. Either pass it directly or set it as an env var:

```python
# Direct
client = RaindropClient(token="your-test-token")

# Via environment variable
# export RAINDROP_TEST_TOKEN=your-test-token
client = RaindropClient()
```

### OAuth2 (for apps acting on behalf of users)

```python
from raindrop_client import OAuth2Auth

auth = OAuth2Auth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    redirect_uri="https://your-app.com/callback",
)

# Step 1: Redirect user to authorize
url = auth.get_authorize_url()

# Step 2: Exchange the code from the callback
tokens = auth.exchange_code(code="authorization-code-from-callback")

# Step 3: Create client with the access token
client = RaindropClient(token=tokens.access_token)

# Step 4: Refresh when expired
new_tokens = auth.refresh_access_token(refresh_token=tokens.refresh_token)
```

## Resource Groups

| Resource | Description | Key Methods |
|----------|-------------|-------------|
| `client.collections` | Bookmark folders | `list_root()`, `create()`, `update()`, `delete()` |
| `client.raindrops` | Bookmarks | `list()`, `create()`, `update()`, `delete()`, `suggest_for_url()` |
| `client.tags` | Tag labels | `list()`, `rename()`, `merge()`, `delete()` |
| `client.user` | User profile | `get()`, `update()`, `get_stats()` |
| `client.highlights` | Text highlights | `list()`, `list_by_collection()` |
| `client.filters` | Facet counts | `get()` |
| `client.sharing` | Collection sharing | `share()`, `get_collaborators()`, `update_access()` |
| `client.import_export` | Import/export | `import_file()`, `export()`, `check_urls()` |
| `client.backups` | Data backups | `list()`, `generate()`, `download()` |

## Special Collection IDs

| ID | Meaning |
|----|---------|
| `0` | All raindrops |
| `-1` | Unsorted (no collection) |
| `-99` | Trash |

## Error Handling

```python
from raindrop_client import RaindropClient, NotFoundError, RateLimitError

client = RaindropClient(token="...")

try:
    raindrop = client.raindrops.get(99999999)
except NotFoundError:
    print("Raindrop not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
```

## Development

```bash
# Setup
uv sync

# Run tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=raindrop_client --cov-report=term-missing
```

## License

MIT
