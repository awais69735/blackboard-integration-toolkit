"""Unit tests for OAuth2 authentication."""

import pytest
import time
from unittest.mock import patch, Mock
from blackboard.infrastructure.http.auth import OAuth2Auth
from blackboard.interfaces.config.settings import AuthSettings
from blackboard.exceptions.blackboard_errors import AuthenticationError


class TestOAuth2Auth:
    def test_get_token_success(self):
        settings = AuthSettings(
            client_id="test",
            client_secret="secret",
            token_url="https://example.com/token"
        )
        with patch("httpx.Client.post") as mock_post:
            mock_post.return_value = Mock(
                status_code=200,
                json=lambda: {"access_token": "abc123", "expires_in": 3600}
            )
            auth = OAuth2Auth(settings)
            token = auth.get_access_token()
            assert token == "abc123"
            # Second call should use cached token
            token2 = auth.get_access_token()
            assert token2 == "abc123"
            assert mock_post.call_count == 1

    def test_token_refresh(self):
        settings = AuthSettings(
            client_id="test",
            client_secret="secret",
            token_url="https://example.com/token"
        )
        with patch("httpx.Client.post") as mock_post:
            mock_post.return_value = Mock(
                status_code=200,
                json=lambda: {"access_token": "new_token", "expires_in": 3600}
            )
            auth = OAuth2Auth(settings)
            # Force expiry
            auth._token_expiry = time.time() - 10
            token = auth.get_access_token()
            assert token == "new_token"
            assert mock_post.call_count == 1

    def test_token_failure(self):
        settings = AuthSettings(
            client_id="test",
            client_secret="secret",
            token_url="https://example.com/token"
        )
        with patch("httpx.Client.post") as mock_post:
            mock_post.side_effect = Exception("Network error")
            auth = OAuth2Auth(settings)
            with pytest.raises(AuthenticationError):
                auth.get_access_token()