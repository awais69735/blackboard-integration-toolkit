"""Unit tests for rate limiter."""

import time
from blackboard.infrastructure.http.rate_limiter import TokenBucketRateLimiter
from blackboard.interfaces.config.settings import RateLimitSettings


class TestTokenBucketRateLimiter:
    def test_acquire_without_limit(self):
        settings = RateLimitSettings(enabled=False, calls_per_second=1, burst=1)
        limiter = TokenBucketRateLimiter(settings)
        start = time.monotonic()
        limiter.acquire()
        elapsed = time.monotonic() - start
        assert elapsed < 0.1  # should not block

    def test_acquire_with_limit(self):
        settings = RateLimitSettings(enabled=True, calls_per_second=2, burst=1)
        limiter = TokenBucketRateLimiter(settings)
        # First acquire should be immediate
        start = time.monotonic()
        limiter.acquire()
        elapsed1 = time.monotonic() - start
        assert elapsed1 < 0.1
        # Second acquire should wait at least 0.5 sec (1/2 rate) if burst=1
        start = time.monotonic()
        limiter.acquire()
        elapsed2 = time.monotonic() - start
        assert elapsed2 >= 0.5