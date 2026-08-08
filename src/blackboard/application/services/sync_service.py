"""Main sync service facade."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from blackboard.application.dto import SyncOptions, SyncResult
from blackboard.application.sync.student_sync import StudentSyncEngine
from blackboard.application.sync.course_sync import CourseSyncEngine
from blackboard.application.sync.enrollment_sync import EnrollmentSyncEngine
from blackboard.application.sync.grade_sync import GradeSyncEngine
from blackboard.infrastructure.providers.blackboard import BlackboardProvider
from blackboard.infrastructure.logging import get_logger
from blackboard.events.event_bus import EventBus, Event

logger = get_logger(__name__)


class SyncService:
    """Facade for synchronisation operations."""

    def __init__(self, provider: BlackboardProvider):
        self.provider = provider

    def sync_students(self, external_students: List[Dict[str, Any]],
                     options: Optional[SyncOptions] = None) -> SyncResult:
        options = options or SyncOptions()
        logger.info("Starting student sync", dry_run=options.dry_run)
        engine = StudentSyncEngine(self.provider, external_students, options)
        result = engine.sync()
        EventBus.emit(Event(name="sync.students.completed", payload=result, source="sync_service"))
        return result

    def sync_courses(self, external_courses: List[Dict[str, Any]],
                    options: Optional[SyncOptions] = None) -> SyncResult:
        options = options or SyncOptions()
        logger.info("Starting course sync", dry_run=options.dry_run)
        engine = CourseSyncEngine(self.provider, external_courses, options)
        result = engine.sync()
        EventBus.emit(Event(name="sync.courses.completed", payload=result, source="sync_service"))
        return result

    def sync_enrollments(self, external_enrollments: List[Dict[str, Any]],
                        options: Optional[SyncOptions] = None) -> SyncResult:
        options = options or SyncOptions()
        logger.info("Starting enrollment sync", dry_run=options.dry_run)
        engine = EnrollmentSyncEngine(self.provider, external_enrollments, options)
        result = engine.sync()
        EventBus.emit(Event(name="sync.enrollments.completed", payload=result, source="sync_service"))
        return result

    def sync_grades(self, external_grades: List[Dict[str, Any]],
                   assignment_id: Optional[str] = None,
                   course_id: Optional[str] = None,
                   options: Optional[SyncOptions] = None) -> SyncResult:
        options = options or SyncOptions()
        logger.info("Starting grade sync", dry_run=options.dry_run, assignment=assignment_id, course=course_id)
        engine = GradeSyncEngine(self.provider, external_grades, assignment_id, course_id, options)
        result = engine.sync()
        EventBus.emit(Event(name="sync.grades.completed", payload=result, source="sync_service"))
        return result