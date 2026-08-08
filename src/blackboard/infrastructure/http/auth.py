"""OAuth2 authentication implementation."""

import time
from typing import Optional, Dict, Any
import httpx
from pydantic import SecretStr

from blackboard.interfaces.config.settings import AuthSettings
from blackboard.exceptions import AuthenticationError
from blackboard.infrastructure.logging import get_logger

logger = get_logger(__name__)


class OAuth2Auth:
    """OAuth2 client credentials flow with automatic token refresh."""

    def __init__(self, settings: AuthSettings, http_client: Optional[httpx.Client] = None):
        self.settings = settings
        self._http_client = http_client or httpx.Client(timeout=settings.auth_timeout)
        self._access_token: Optional[str] = None
        self._token_expiry: float = 0.0

    def _request_token(self) -> Dict[str, Any]:
        try:
            response = self._http_client.post(
                self.settings.token_url,
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.settings.client_id,
                    "client_secret": self.settings.client_secret.get_secret_value(),
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error("Token request failed", error=str(e))
            raise AuthenticationError(f"Failed to obtain access token: {e}") from e
    
    def get_access_token(self) -> str:
        if self._access_token and time.time() < self._token_expiry:
            return self._access_token

        logger.info("Obtaining new access token")
        token_data = self._request_token()
        self._access_token = token_data["access_token"]
        expires_in = token_data.get("expires_in", 3600) - 10
        self._token_expiry = time.time() + expires_in
        logger.debug("Token obtained", expires_in=expires_in)
        return self._access_token

    def refresh(self) -> str:
        self._access_token = None
        self._token_expiry = 0.0
        return self.get_access_token()

    def __call__(self, request: httpx.Request) -> httpx.Request:
        token = self.get_access_token()
        request.headers["Authorization"] = f"Bearer {token}"
        return request