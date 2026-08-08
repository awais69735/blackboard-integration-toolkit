"""Custom exception hierarchy for the Blackboard Integration Toolkit."""

from .blackboard_errors import (
    BlackboardError,
    AuthenticationError,
    ResourceNotFoundError,
    RateLimitExceededError,
    ValidationError,
)

__all__ = [
    "BlackboardError",
    "AuthenticationError",
    "ResourceNotFoundError",
    "RateLimitExceededError",
    "ValidationError",
]