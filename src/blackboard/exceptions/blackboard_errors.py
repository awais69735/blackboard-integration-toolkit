"""Custom exception classes."""

class BlackboardError(Exception):
    """Base exception for all toolkit errors."""

class AuthenticationError(BlackboardError):
    """Authentication failed (OAuth2 token issue)."""

class ResourceNotFoundError(BlackboardError):
    """Requested resource (student, course, etc.) does not exist."""

class RateLimitExceededError(BlackboardError):
    """Rate limit has been exceeded; retry after backoff."""

class ValidationError(BlackboardError):
    """Invalid data provided to the API (e.g., missing fields)."""

class ConfigurationError(BlackboardError):
    """Invalid or missing configuration settings."""