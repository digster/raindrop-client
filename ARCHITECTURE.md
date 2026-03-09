# Architecture

## Big Picture

```
┌─────────────────────────────────────────────────┐
│                RaindropClient                    │
│  (client.py — single entry point / facade)       │
│                                                   │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │collections│ │raindrops │ │  tags    │ ...      │
│  │ Resource  │ │ Resource │ │ Resource │          │
│  └─────┬────┘ └─────┬────┘ └─────┬────┘          │
│        │            │            │                 │
│        └────────────┼────────────┘                 │
│                     ▼                              │
│           ┌─────────────────┐                      │
│           │  HttpTransport  │                      │
│           │   (http.py)     │                      │
│           │  rate limiting  │                      │
│           │  retry logic    │                      │
│           │  error mapping  │                      │
│           └────────┬────────┘                      │
│                    │                               │
└────────────────────┼───────────────────────────────┘
                     ▼
            Raindrop.io REST API
```

## Layers

### 1. Client Facade (`client.py`)
- Single entry point: `RaindropClient(token=...)`
- Resolves token from param or `RAINDROP_TEST_TOKEN` env var
- Creates shared `HttpTransport` and initializes all resource groups
- Context manager support for automatic cleanup

### 2. Resource Groups (`resources/`)
- Each file wraps a set of related API endpoints
- Methods accept typed request objects or `**kwargs` for convenience
- Parse API JSON responses into Pydantic models
- Resource groups: `collections`, `raindrops`, `tags`, `user`, `highlights`, `filters`, `sharing`, `import_export`, `backups`

### 3. HTTP Transport (`http.py`)
- Wraps `httpx.Client` with Bearer auth headers
- Rate limit retry: parses `X-RateLimit-Reset` header, sleeps + retries up to 3 times on 429
- Error mapping: HTTP status codes → typed exception hierarchy
- Methods: `get()`, `post()`, `put()`, `delete()`, `upload()`, `upload_post()`, `download()`

### 4. Pydantic Models (`models/`)
- Response models: parse API JSON with `model_validate()`
- Request models: `to_api_body()` method serializes to API format
- `ConfigDict(extra="ignore")` — unknown API fields don't break parsing
- `Field(alias="_id")` / `Field(alias="$id")` — maps MongoDB-style IDs to Python names

### 5. Auth (`auth.py`)
- `OAuth2Auth`: full authorization code flow (authorize URL → code exchange → token refresh)
- Test token: passed directly to `RaindropClient(token=...)`
- Stateless — token storage is the caller's responsibility

### 6. Exceptions (`exceptions.py`)
- `RaindropError` base class with `status_code` and `response_body`
- Specific subclasses: `AuthenticationError` (401), `NotFoundError` (404), `RateLimitError` (429), etc.

## Key Design Decisions

1. **Sync-only**: Uses `httpx.Client` (sync), not `httpx.AsyncClient`. Simpler for scripting and LLM use.
2. **Pydantic v2 with `extra="ignore"`**: Forward-compatible with API changes.
3. **Resource pattern**: Same as Stripe/Twilio SDKs — `client.resource.method()`.
4. **`to_api_body()` on request models**: Encapsulates `$id` nesting and field exclusion logic.
5. **No token storage**: Library stays stateless — callers manage their own tokens.

## Data Flow

```
User code → Resource method → HttpTransport._request() → httpx → API
                ↓                       ↓
        Pydantic model_validate()   Rate limit retry
                                    Error → Exception mapping
```

## Special Values

| Constant | Value | Usage |
|----------|-------|-------|
| `COLLECTION_ALL` | `0` | All raindrops across collections |
| `COLLECTION_UNSORTED` | `-1` | Raindrops not in any collection |
| `COLLECTION_TRASH` | `-99` | Trash bin |

## Testing

- **respx** mocks httpx at the transport level — no real HTTP calls
- **Factory functions** in `conftest.py` produce consistent test data
- Test structure mirrors source: `test_models/` and `test_resources/`
- Run: `uv run pytest -v --cov=raindrop_client`
