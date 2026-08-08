"""Base sync engine with common functionality."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, TypeVar, Generic
from datetime import datetime, timezone
import logging

from blackboard.application.dto import SyncOptions, SyncResult, SyncDiff, SyncStatus, SyncAction
from blackboard.infrastructure.logging import get_logger

T = TypeVar('T')  # Entity type
K = TypeVar('K')  # ID type
logger = get_logger(__name__)


class BaseSyncEngine(ABC, Generic[T, K]):
    """Base class for all sync engines."""
    
    def __init__(self, options: SyncOptions):
        self.options = options
        self.batch_size = options.batch_size
        self.dry_run = options.dry_run
        
    @abstractmethod
    def get_external_data(self) -> List[Dict[str, Any]]:
        """Fetch data from the external system (SIS, ERP, etc.)."""
        pass
    
    @abstractmethod
    def get_blackboard_data(self) -> List[T]:
        """Fetch data from Blackboard."""
        pass
    @abstractmethod
    def get_external_id_from_data(self, data: Dict[str, Any]) -> str:
        """Extract the external ID from a data dict."""
        pass

    @abstractmethod
    def find_external_id(self, entity: T) -> str:
        """Extract the external ID from a Blackboard entity."""
        pass
    
    @abstractmethod
    def create_in_blackboard(self, data: Dict[str, Any]) -> T:
        """Create a new entity in Blackboard."""
        pass
    
    @abstractmethod
    def update_in_blackboard(self, entity: T, data: Dict[str, Any]) -> T:
        """Update an existing entity in Blackboard."""
        pass
    
    @abstractmethod
    def delete_in_blackboard(self, entity: T) -> None:
        """Delete an entity from Blackboard."""
        pass
    
    @abstractmethod
    def compare(self, external_data: Dict[str, Any], blackboard_data: T) -> Optional[Dict[str, Any]]:
        """
        Compare external data with Blackboard data.
        Returns dict of changed fields, or None if no changes.
        """
        pass
    
    def sync(self) -> SyncResult:
        """Execute the sync operation."""
        result = SyncResult(status=SyncStatus.SUCCESS)
        
        try:
            # Fetch data
            external_data = self.get_external_data()
            blackboard_data = self.get_blackboard_data()
            
            # Build index for Blackboard data
            bb_index: Dict[str, T] = {}
            for entity in blackboard_data:
                ext_id = self.find_external_id(entity)
                if ext_id:
                    bb_index[ext_id] = entity
            
            # Process diffs
            diffs = self._calculate_diffs(external_data, bb_index)
            result = self._apply_diffs(diffs, result)
            
        except Exception as e:
            logger.error("Sync failed", error=str(e))
            result.status = SyncStatus.FAILED
            result.errors.append(str(e))
        
        result.completed_at = datetime.now(timezone.utc)
        return result
    
    def _calculate_diffs(self, external_data: List[Dict[str, Any]], 
                         bb_index: Dict[str, T]) -> List[SyncDiff]:
        """Calculate differences between external and Blackboard data."""
        diffs = []
        processed_ids = set()
        
        # Check for updates and creations
        for ext_item in external_data:
            ext_id = ext_item.get('id')
            if not ext_id:
                continue
            processed_ids.add(ext_id)
            
            if ext_id in bb_index:
                # Update or skip
                bb_entity = bb_index[ext_id]
                changes = self.compare(ext_item, bb_entity)
                if changes:
                    diffs.append(SyncDiff(
                        action=SyncAction.UPDATE,
                        external_id=ext_id,
                        blackboard_id=self.find_external_id(bb_entity),
                        external_data=ext_item,
                        blackboard_data=bb_entity,
                        changes=changes
                    ))
                else:
                    diffs.append(SyncDiff(
                        action=SyncAction.SKIP,
                        external_id=ext_id,
                        blackboard_id=None,
                        external_data=ext_item,
                        blackboard_data=bb_entity,
                        changes={}
                    ))
            else:
                # Create new
                diffs.append(SyncDiff(
                    action=SyncAction.CREATE,
                    external_id=ext_id,
                    blackboard_id=None,
                    external_data=ext_item,
                    blackboard_data=None,
                    changes={}
                ))
        
        # Check for deletions
        if self.options.full_refresh:
            for ext_id, bb_entity in bb_index.items():
                if ext_id not in processed_ids:
                    diffs.append(SyncDiff(
                        action=SyncAction.DELETE,
                        external_id=ext_id,
                        blackboard_id=self.find_external_id(bb_entity),
                        external_data={},
                        blackboard_data=bb_entity,
                        changes={}
                    ))
        
        return diffs
    
    def _apply_diffs(self, diffs: List[SyncDiff], result: SyncResult) -> SyncResult:
        """Apply diffs to Blackboard."""
        for diff in diffs:
            if self.dry_run:
                result.status = SyncStatus.DRY_RUN
                continue
            
            try:
                if diff.action == SyncAction.CREATE:
                    self.create_in_blackboard(diff.external_data)
                    result.created += 1
                    
                elif diff.action == SyncAction.UPDATE:
                    self.update_in_blackboard(diff.blackboard_data, diff.external_data)
                    result.updated += 1
                    
                elif diff.action == SyncAction.DELETE:
                    self.delete_in_blackboard(diff.blackboard_data)
                    result.deleted += 1
                    
                elif diff.action == SyncAction.SKIP:
                    result.skipped += 1
                    
            except Exception as e:
                logger.error(f"Failed to {diff.action.value}", 
                           ext_id=diff.external_id, error=str(e))
                result.errors.append(f"{diff.action.value} {diff.external_id}: {e}")
                result.status = SyncStatus.PARTIAL
        
        return result