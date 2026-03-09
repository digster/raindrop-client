# Raindrop.io API Client — Claude Code Skill

Use the `raindrop_client` Python library to interact with the Raindrop.io bookmark manager API.

## Quick Start

```python
from raindrop_client import RaindropClient

# Requires RAINDROP_TEST_TOKEN env var or explicit token
client = RaindropClient(token="your-test-token")
```

## Resource Groups & Methods

### Collections (folders)
```python
client.collections.list_root()                           # All root collections
client.collections.list_children()                       # All nested collections
client.collections.get(collection_id)                    # Single collection
client.collections.create(title="Name", view="list")     # Create
client.collections.update(collection_id, title="New")     # Update
client.collections.delete(collection_id)                 # Delete (moves to trash)
client.collections.upload_cover(id, file_bytes, "c.jpg") # Upload cover image
client.collections.reorder(sort="title")                 # Reorder all
client.collections.merge([id1, id2], to=target_id)       # Merge collections
client.collections.empty_trash()                         # Empty trash
client.collections.delete_many([id1, id2])               # Bulk delete
```

### Raindrops (bookmarks)
```python
client.raindrops.get(raindrop_id)                        # Single raindrop
client.raindrops.create(link="https://...", tags=["ai"])  # Create bookmark
client.raindrops.update(raindrop_id, title="New Title")   # Update
client.raindrops.delete(raindrop_id)                     # Delete

# List with search, sort, pagination
client.raindrops.list(
    collection_id=0,      # 0=all, -1=unsorted, -99=trash
    search="python",
    sort="-created",      # -created, title, -sort, score
    page=0,
    perpage=25,           # max 50
)

# Bulk operations
client.raindrops.create_many([{"link": "https://a.com"}, {"link": "https://b.com"}])
client.raindrops.update_many(ids=[1, 2], important=True)
client.raindrops.delete_many(collection_id=-99, ids=[1, 2])

# File & cover upload
client.raindrops.upload_file(collection_id, file_bytes, "doc.pdf")
client.raindrops.upload_cover(raindrop_id, img_bytes, "cover.jpg")

# Suggestions & cache
client.raindrops.suggest_for_url("https://example.com")
client.raindrops.suggest_for_existing(raindrop_id)
client.raindrops.get_cache(raindrop_id)  # Returns bytes
```

### Tags
```python
client.tags.list()                                        # All tags
client.tags.list(collection_id=12345)                    # Tags in collection
client.tags.rename(tags=["old"], replace="new")           # Rename
client.tags.merge(tags=["a", "b"], replace="merged")     # Merge tags
client.tags.delete(tags=["unwanted"])                    # Delete
```

### User
```python
client.user.get()                                        # Current user profile
client.user.update(full_name="New Name")                  # Update profile
client.user.get_public("username")                        # Public profile
client.user.get_stats()                                   # Account stats
client.user.disconnect("google")                          # Disconnect service
```

### Highlights
```python
client.highlights.list(raindrop_id)                      # Highlights for raindrop
client.highlights.list_by_collection(collection_id=0)    # All highlights
```

### Filters
```python
client.filters.get(collection_id=0)                      # Facet counts
# Returns: broken, duplicates, important, notag counts + tag/type facets
```

### Sharing
```python
client.sharing.get_collaborators(collection_id)
client.sharing.share(collection_id, role="viewer", emails=["user@example.com"])
client.sharing.update_access(collection_id, user_id, role="member")
client.sharing.remove_collaborator(collection_id, user_id)
client.sharing.unshare(collection_id)
client.sharing.accept(token="invite-token")
```

### Import/Export
```python
client.import_export.parse_url("https://example.com")    # Extract metadata
client.import_export.check_urls(["https://a.com"])        # Check if URLs exist
client.import_export.import_file(html_bytes)              # Import HTML bookmarks
client.import_export.export(collection_id=0, format="csv") # Export (csv/html/zip)
```

### Backups
```python
client.backups.list()                                     # List backups
client.backups.generate()                                 # Trigger new backup
client.backups.download("backup-id")                      # Download (returns bytes)
```

## Special Collection IDs
- `0` — All raindrops
- `-1` — Unsorted (no collection)
- `-99` — Trash

## Error Handling
```python
from raindrop_client import NotFoundError, RateLimitError, AuthenticationError

try:
    client.raindrops.get(99999999)
except NotFoundError:
    print("Not found")
except RateLimitError as e:
    print(f"Rate limited, retry after {e.retry_after}s")
except AuthenticationError:
    print("Invalid token")
```

## Environment Variables
- `RAINDROP_TEST_TOKEN` — Test token (from Raindrop.io integrations settings)
- `RAINDROP_CLIENT_ID` — OAuth2 client ID (optional)
- `RAINDROP_CLIENT_SECRET` — OAuth2 client secret (optional)
- `RAINDROP_REDIRECT_URI` — OAuth2 redirect URI (optional)
