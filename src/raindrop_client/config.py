"""Configuration constants and environment variable names for the Raindrop.io API client."""

# API base URL
API_BASE_URL = "https://api.raindrop.io"

# OAuth2 endpoints (hosted on raindrop.io, not api.raindrop.io)
OAUTH_AUTHORIZE_URL = "https://raindrop.io/oauth/authorize"
OAUTH_TOKEN_URL = "https://raindrop.io/oauth/access_token"

# API version prefix
API_PREFIX = "/rest/v1"

# Environment variable names
ENV_TEST_TOKEN = "RAINDROP_TEST_TOKEN"
ENV_CLIENT_ID = "RAINDROP_CLIENT_ID"
ENV_CLIENT_SECRET = "RAINDROP_CLIENT_SECRET"
ENV_REDIRECT_URI = "RAINDROP_REDIRECT_URI"

# Rate limiting
RATE_LIMIT_MAX_RETRIES = 3
RATE_LIMIT_DEFAULT_WAIT = 5  # seconds, fallback if no Reset header

# Pagination
DEFAULT_PER_PAGE = 25
MAX_PER_PAGE = 50

# Special collection IDs
COLLECTION_ALL = 0
COLLECTION_UNSORTED = -1
COLLECTION_TRASH = -99

# Request timeout (seconds)
DEFAULT_TIMEOUT = 30
