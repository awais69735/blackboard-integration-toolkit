"""HTTP client with retries, auth, rate limiting, and logging."""

import time
import httpx
from typing import Optional, Dict, Any
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception,
)

from blackboard.interfaces.config.settings import HttpSettings
from blackboard.exceptions import (
    BlackboardError,
    AuthenticationError,
    RateLimitExceededError,
    ResourceNotFoundError,
    ValidationError,
)
from .auth import OAuth2Auth
from .rate_limiter import TokenBucketRateLimiter
from blackboard.infrastructure.logging import get_logger

logger = get_logger(__name__)


class HTTPClient:
    """HTTP client with built‑in retries, authentication, and rate limiting."""

    def __init__(
        self,
        auth: OAuth2Auth,
        settings: HttpSettings,
        rate_limiter: TokenBucketRateLimiter,
        timeout: Optional[int] = None,
    ):
        self.auth = auth
        self.settings = settings
        self.rate_limiter = rate_limiter
        self.timeout = timeout or settings.timeout

        self._client = httpx.Client(
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(
                max_keepalive_connections=settings.pool_connections,
                max_connections=settings.pool_maxsize,
            ),
            auth=self.auth,
            base_url=settings.base_url,
        )

    @staticmethod
    def _should_retry(exception: Exception) -> bool:
        if isinstance(exception, httpx.HTTPStatusError):
            status = exception.response.status_code
            return status in (429, 500, 502, 503, 504, 408, 409)
        return False

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_exception(_should_retry),  # works because it's static
        reraise=True,
    )
    
    def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        self.rate_limiter.acquire()

        start_time = time.time()
        logger.debug("Sending request", method=method, url=url, params=params)

        try:
            response = self._client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                headers=headers,
            )
            response.raise_for_status()
            elapsed = time.time() - start_time
            logger.debug(
                "Request successful",
                status_code=response.status_code,
                elapsed=f"{elapsed:.3f}s"
            )
            return response
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            elapsed = time.time() - start_time
            logger.warning(
                "HTTP error",
                status_code=status,
                url=url,
                elapsed=f"{elapsed:.3f}s",
                error=str(e)
            )
            if status == 401:
                raise AuthenticationError("Authentication failed") from e
            elif status == 404:
                raise ResourceNotFoundError(f"Resource not found: {url}") from e
            elif status == 429:
                raise RateLimitExceededError("Rate limit exceeded") from e
            elif 400 <= status < 500:
                raise ValidationError(f"Client error {status}: {e.response.text}") from e
            else:
                raise BlackboardError(f"HTTP {status}: {e.response.text}") from e
        except httpx.TimeoutException as e:
            logger.error("Request timeout", url=url)
            raise
        except Exception as e:
            logger.error("Unexpected error", url=url, error=str(e))
            raise BlackboardError(f"Request failed: {e}") from e

    def get(self, url: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> httpx.Response:
        return self._request("GET", url, params=params, headers=headers)

    def post(self, url: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> httpx.Response:
        return self._request("POST", url, json=json, headers=headers)

    def patch(self, url: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> httpx.Response:
        return self._request("PATCH", url, json=json, headers=headers)

    def put(self, url: str, json: Optional[Dict] = None, headers: Optional[Dict] = None) -> httpx.Response:
        return self._request("PUT", url, json=json, headers=headers)

    def delete(self, url: str, headers: Optional[Dict] = None) -> httpx.Response:
        return self._request("DELETE", url, headers=headers)