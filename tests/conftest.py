import pytest
import httpx
from flask import Flask
from blackboard.infrastructure.http.client import HTTPClient
from blackboard.infrastructure.http.auth import OAuth2Auth
from blackboard.infrastructure.http.rate_limiter import TokenBucketRateLimiter
from blackboard.interfaces.config.settings import AuthSettings, HttpSettings, RateLimitSettings
from blackboard.infrastructure.providers.blackboard import BlackboardProvider
from tests.integration.mock_blackboard.server import create_app


@pytest.fixture(scope="function")
def mock_app() -> Flask:
    return create_app()


@pytest.fixture(scope="function")
def http_client(mock_app) -> HTTPClient:
    auth_settings = AuthSettings(
        client_id="test",
        client_secret="secret",
        token_url="https://example.com/token"
    )
    http_settings = HttpSettings(
        base_url="http://mock",
        timeout=30
    )
    rate_settings = RateLimitSettings(enabled=False)

    auth = OAuth2Auth(auth_settings)
    auth._access_token = "dummy_token"
    auth._token_expiry = float('inf')

    rate_limiter = TokenBucketRateLimiter(rate_settings)

    client = HTTPClient(
        auth=auth,
        settings=http_settings,
        rate_limiter=rate_limiter
    )
    transport = httpx.WSGITransport(app=mock_app)
    client._client = httpx.Client(transport=transport, base_url="http://mock")
    return client


@pytest.fixture(scope="function")
def blackboard_provider(http_client) -> BlackboardProvider:
    return BlackboardProvider(http_client)