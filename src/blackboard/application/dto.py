"""Data Transfer Objects for sync operations."""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict
from datetime import datetime
from enum import Enum


class SyncAction(Enum):
    """Action to be performed during sync."""
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    SKIP = "skip"


class SyncStatus(Enum):
    """Status of a sync operation."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    DRY_RUN = "dry_run"


@dataclass
class SyncOptions:
    """Options for sync operations."""
    dry_run: bool = False
    batch_size: int = 100
    full_refresh: bool = False
    active_only: bool = True
    external_source: Optional[str] = None
    filters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SyncResult:
    """Result of a sync operation."""
    status: SyncStatus
    created: int = 0
    updated: int = 0
    deleted: int = 0
    skipped: int = 0
    errors: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None


@dataclass
class SyncDiff:
    """Represents a difference between external and Blackboard data."""
    action: SyncAction
    external_id: str
    blackboard_id: Optional[str]
    external_data: Dict[str, Any]
    blackboard_data: Optional[Dict[str, Any]]
    changes: Dict[str, Any] = field(default_factory=dict)