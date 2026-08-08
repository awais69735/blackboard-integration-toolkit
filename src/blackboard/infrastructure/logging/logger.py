"""Structured logging setup using structlog."""

import structlog
import sys
from typing import Any, Dict, Optional
from blackboard.interfaces.config.settings import LoggingSettings


def configure_logging(settings: LoggingSettings) -> None:
    """Configure structlog based on settings."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.json_format:
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer()
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer()
        ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Also configure standard logging for libraries that use it
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.level.upper(), logging.INFO)
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """Get a structlog logger with optional context."""
    return structlog.get_logger(name)