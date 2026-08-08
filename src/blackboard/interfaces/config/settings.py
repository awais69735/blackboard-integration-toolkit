"""Configuration management with Pydantic."""

from pydantic import BaseModel, Field
from typing import Optional
from pydantic import SecretStr
import os
from dotenv import load_dotenv


class AuthSettings(BaseModel):
    """OAuth2 authentication settings."""
    client_id: str = Field(..., env="BB_CLIENT_ID")
    client_secret: SecretStr = Field(..., env="BB_CLIENT_SECRET")
    token_url: str = Field(..., env="BB_TOKEN_URL")
    auth_timeout: int = Field(30, env="BB_AUTH_TIMEOUT")


class HttpSettings(BaseModel):
    """HTTP client settings."""
    base_url: str = Field(..., env="BB_BASE_URL")
    timeout: int = Field(60, env="BB_TIMEOUT")
    max_retries: int = Field(3, env="BB_MAX_RETRIES")
    retry_backoff: float = Field(1.0, env="BB_RETRY_BACKOFF")
    pool_connections: int = Field(100, env="BB_POOL_CONNECTIONS")
    pool_maxsize: int = Field(100, env="BB_POOL_MAXSIZE")


class RateLimitSettings(BaseModel):
    """Rate limiting settings."""
    enabled: bool = Field(True, env="BB_RATE_LIMIT_ENABLED")
    calls_per_second: float = Field(5.0, env="BB_RATE_LIMIT_CALLS_PER_SECOND")
    burst: int = Field(10, env="BB_RATE_LIMIT_BURST")


class PaginationSettings(BaseModel):
    """Default pagination settings."""
    default_limit: int = Field(100, env="BB_DEFAULT_LIMIT")
    max_limit: int = Field(1000, env="BB_MAX_LIMIT")


class LoggingSettings(BaseModel):
    """Logging settings."""
    level: str = Field("INFO", env="BB_LOG_LEVEL")
    json_format: bool = Field(False, env="BB_LOG_JSON")


class Settings(BaseModel):
    """Master configuration aggregator."""
    auth: AuthSettings
    http: HttpSettings
    rate_limit: RateLimitSettings
    pagination: PaginationSettings
    logging: LoggingSettings

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "Settings":
        """Load settings from environment variables and optional .env file."""
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()  # look for .env by default

        # We'll use Pydantic's env parsing via the Field(..., env=...)
        # But we need to instantiate the nested models manually.
        return cls(
            auth=AuthSettings(
                client_id=os.getenv("BB_CLIENT_ID", ""),
                client_secret=SecretStr(os.getenv("BB_CLIENT_SECRET", "")),
                token_url=os.getenv("BB_TOKEN_URL", ""),
                auth_timeout=int(os.getenv("BB_AUTH_TIMEOUT", "30")),
            ),
            http=HttpSettings(
                base_url=os.getenv("BB_BASE_URL", ""),
                timeout=int(os.getenv("BB_TIMEOUT", "60")),
                max_retries=int(os.getenv("BB_MAX_RETRIES", "3")),
                retry_backoff=float(os.getenv("BB_RETRY_BACKOFF", "1.0")),
                pool_connections=int(os.getenv("BB_POOL_CONNECTIONS", "100")),
                pool_maxsize=int(os.getenv("BB_POOL_MAXSIZE", "100")),
            ),
            rate_limit=RateLimitSettings(
                enabled=os.getenv("BB_RATE_LIMIT_ENABLED", "true").lower() in ("true", "1", "yes"),
                calls_per_second=float(os.getenv("BB_RATE_LIMIT_CALLS_PER_SECOND", "5.0")),
                burst=int(os.getenv("BB_RATE_LIMIT_BURST", "10")),
            ),
            pagination=PaginationSettings(
                default_limit=int(os.getenv("BB_DEFAULT_LIMIT", "100")),
                max_limit=int(os.getenv("BB_MAX_LIMIT", "1000")),
            ),
            logging=LoggingSettings(
                level=os.getenv("BB_LOG_LEVEL", "INFO"),
                json_format=os.getenv("BB_LOG_JSON", "false").lower() in ("true", "1", "yes"),
            ),
        )