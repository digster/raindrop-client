# Prompts

## 2026-03-09 — Initial Implementation

Implement the following plan:

Build a Python client library for the Raindrop.io API — designed for developers and LLMs, not end users. The library wraps all Raindrop.io REST API v1 endpoints with typed Pydantic models, clean resource-grouped methods, and built-in rate limiting/retry. A Claude Code skill file is included so LLMs can use the library directly.

Key requirements:
- Pydantic v2 models with `ConfigDict(extra="ignore")` and `Field(alias="_id")`/`Field(alias="$id")`
- `HttpTransport` wrapping httpx (sync) with rate limit retry and error mapping
- Resource-grouped client facade: `client.collections`, `client.raindrops`, `client.tags`, etc.
- Both OAuth2 and test token authentication
- Exception hierarchy mapping HTTP status codes
- Full API coverage: Collections, Raindrops, Tags, User, Highlights, Filters, Sharing, Import/Export, Backups
- Comprehensive test suite using respx for HTTP mocking
- Documentation: README.md, ARCHITECTURE.md, skill.md
