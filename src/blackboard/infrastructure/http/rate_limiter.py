"""Rate limiter implementation using token bucket algorithm."""

import time
import threading
from blackboard.interfaces.config.settings import RateLimitSettings
from blackboard.exceptions.blackboard_errors import RateLimitExceededError


class TokenBucketRateLimiter:
    """Thread‑safe token bucket rate limiter."""

    def __init__(self, settings: RateLimitSettings):
        self.settings = settings
        self.capacity = settings.burst
        self.tokens = self.capacity
        self.rate = settings.calls_per_second  # tokens per second
        self.last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self) -> None:
        """Refill tokens based on elapsed time."""
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now

    def consume(self, tokens: int = 1) -> float:
        """
        Consume tokens and return wait time if not enough tokens.
        If tokens are insufficient, sleep for the required time and then consume.
        """
        if not self.settings.enabled:
            return 0.0

        with self._lock:
            self._refill()
            if self.tokens >= tokens:
                self.tokens -= tokens
                return 0.0
            # Not enough tokens, calculate wait time
            required_tokens = tokens - self.tokens
            wait_time = required_tokens / self.rate
            # We'll sleep outside the lock after releasing it
            # But we need to adjust tokens after sleep.
            # Simpler: we'll set a sleep and return the wait time.
            # We'll handle sleep in the consumer.
            return wait_time

    def acquire(self, tokens: int = 1) -> None:
        """Acquire tokens, blocking if necessary."""
        wait = self.consume(tokens)
        if wait > 0:
            time.sleep(wait)
            # After sleep, we need to consume again (maybe other threads consumed)
            # For simplicity, we'll just sleep and then retry consume.
            # We'll use a loop to ensure we get tokens.
            while True:
                with self._lock:
                    self._refill()
                    if self.tokens >= tokens:
                        self.tokens -= tokens
                        break
                    # Not enough, sleep more
                    required_tokens = tokens - self.tokens
                    sleep_time = required_tokens / self.rate
                time.sleep(sleep_time)