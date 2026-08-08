"""Simple event bus for extensibility."""

from typing import Dict, List, Callable, Any
from dataclasses import dataclass


@dataclass
class Event:
    """Base event class."""
    name: str
    payload: Any
    source: str = None


class EventBus:
    """Simple in-memory event bus."""

    _handlers: Dict[str, List[Callable]] = {}

    @classmethod
    def register(cls, event_name: str, handler: Callable) -> None:
        """Register a handler for an event."""
        if event_name not in cls._handlers:
            cls._handlers[event_name] = []
        cls._handlers[event_name].append(handler)

    @classmethod
    def emit(cls, event: Event) -> None:
        """Emit an event to all registered handlers."""
        if event.name in cls._handlers:
            for handler in cls._handlers[event.name]:
                handler(event)

    @classmethod
    def clear(cls) -> None:
        """Clear all handlers (useful for testing)."""
        cls._handlers.clear()