"""OAuth2 authentication flow for the Raindrop.io API.

Supports both the full OAuth2 authorization code flow (for apps acting on
behalf of users) and simple test token authentication (for personal use).

Token storage is the caller's responsibility — this module stays stateless.
"""

from urllib.parse import urlencode

import httpx

from raindrop_client.config import OAUTH_AUTHORIZE_URL, OAUTH_TOKEN_URL
from raindrop_client.exceptions import AuthenticationError


class TokenResponse:
    """Result of a token exchange or refresh."""

    def __init__(self, data: dict):
        self.access_token: str = data.get("access_token", "")
        self.refresh_token: str = data.get("refresh_token", "")
        self.expires_in: int = data.get("expires_in", 0)
        self.token_type: str = data.get("token_type", "Bearer")

    def __repr__(self) -> str:
        return f"TokenResponse(token_type={self.token_type!r}, expires_in={self.expires_in})"


class OAuth2Auth:
    """Handles the OAuth2 authorization code flow for Raindrop.io.

    Usage:
        auth = OAuth2Auth(client_id="...", client_secret="...", redirect_uri="...")

        # Step 1: Get the URL to redirect the user to
        url = auth.get_authorize_url()

        # Step 2: After user authorizes, exchange the code for tokens
        tokens = auth.exchange_code(code="...")

        # Step 3: Later, refresh the access token
        tokens = auth.refresh_access_token(refresh_token="...")
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorize_url(self) -> str:
        """Build the OAuth2 authorization URL to redirect the user to."""
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
        }
        return f"{OAUTH_AUTHORIZE_URL}?{urlencode(params)}"

    def exchange_code(self, code: str) -> TokenResponse:
        """Exchange an authorization code for access and refresh tokens.

        Args:
            code: The authorization code from the OAuth2 callback.

        Returns:
            TokenResponse with access_token, refresh_token, and expiry.

        Raises:
            AuthenticationError: If the code exchange fails.
        """
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }

        response = httpx.post(OAUTH_TOKEN_URL, json=payload)

        if not response.is_success:
            body = {}
            try:
                body = response.json()
            except Exception:
                pass
            error_msg = body.get("error", f"Token exchange failed with status {response.status_code}")
            raise AuthenticationError(str(error_msg), status_code=response.status_code, response_body=body)

        return TokenResponse(response.json())

    def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh an expired access token using a refresh token.

        Args:
            refresh_token: The refresh token from a previous token exchange.

        Returns:
            TokenResponse with new access_token and expiry.

        Raises:
            AuthenticationError: If the refresh fails.
        """
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = httpx.post(OAUTH_TOKEN_URL, json=payload)

        if not response.is_success:
            body = {}
            try:
                body = response.json()
            except Exception:
                pass
            error_msg = body.get("error", f"Token refresh failed with status {response.status_code}")
            raise AuthenticationError(str(error_msg), status_code=response.status_code, response_body=body)

        return TokenResponse(response.json())
