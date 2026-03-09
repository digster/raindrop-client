"""Tests for OAuth2 authentication flow."""

import httpx
import pytest
import respx

from raindrop_client.auth import OAuth2Auth, TokenResponse
from raindrop_client.config import OAUTH_AUTHORIZE_URL, OAUTH_TOKEN_URL
from raindrop_client.exceptions import AuthenticationError


class TestOAuth2Auth:
    """Tests for the OAuth2Auth class."""

    def setup_method(self):
        self.auth = OAuth2Auth(
            client_id="test-client-id",
            client_secret="test-client-secret",
            redirect_uri="https://example.com/callback",
        )

    def test_authorize_url(self):
        """get_authorize_url builds correct OAuth2 authorize URL."""
        url = self.auth.get_authorize_url()
        assert url.startswith(OAUTH_AUTHORIZE_URL)
        assert "client_id=test-client-id" in url
        assert "redirect_uri=" in url

    def test_exchange_code_success(self):
        """exchange_code returns TokenResponse on success."""
        with respx.mock:
            respx.post(OAUTH_TOKEN_URL).respond(200, json={
                "access_token": "access-123",
                "refresh_token": "refresh-456",
                "expires_in": 1209599,
                "token_type": "Bearer",
            })

            result = self.auth.exchange_code(code="auth-code-789")

            assert isinstance(result, TokenResponse)
            assert result.access_token == "access-123"
            assert result.refresh_token == "refresh-456"
            assert result.expires_in == 1209599
            assert result.token_type == "Bearer"

    def test_exchange_code_failure(self):
        """exchange_code raises AuthenticationError on failure."""
        with respx.mock:
            respx.post(OAUTH_TOKEN_URL).respond(400, json={
                "error": "bad_authorization_code",
            })

            with pytest.raises(AuthenticationError, match="bad_authorization_code"):
                self.auth.exchange_code(code="invalid-code")

    def test_refresh_token_success(self):
        """refresh_access_token returns new TokenResponse."""
        with respx.mock:
            respx.post(OAUTH_TOKEN_URL).respond(200, json={
                "access_token": "new-access-789",
                "refresh_token": "new-refresh-012",
                "expires_in": 1209599,
                "token_type": "Bearer",
            })

            result = self.auth.refresh_access_token(refresh_token="old-refresh-456")

            assert result.access_token == "new-access-789"
            assert result.refresh_token == "new-refresh-012"

    def test_refresh_token_failure(self):
        """refresh_access_token raises AuthenticationError on failure."""
        with respx.mock:
            respx.post(OAUTH_TOKEN_URL).respond(401, json={
                "error": "invalid_refresh_token",
            })

            with pytest.raises(AuthenticationError):
                self.auth.refresh_access_token(refresh_token="expired-token")


class TestTokenResponse:
    """Tests for the TokenResponse data class."""

    def test_token_response_from_dict(self):
        """TokenResponse correctly parses API response dict."""
        data = {
            "access_token": "abc",
            "refresh_token": "def",
            "expires_in": 3600,
            "token_type": "Bearer",
        }
        token = TokenResponse(data)
        assert token.access_token == "abc"
        assert token.refresh_token == "def"
        assert token.expires_in == 3600

    def test_token_response_defaults(self):
        """TokenResponse provides defaults for missing fields."""
        token = TokenResponse({})
        assert token.access_token == ""
        assert token.refresh_token == ""
        assert token.expires_in == 0
        assert token.token_type == "Bearer"

    def test_repr(self):
        """TokenResponse repr is informative."""
        token = TokenResponse({"token_type": "Bearer", "expires_in": 3600})
        assert "Bearer" in repr(token)
