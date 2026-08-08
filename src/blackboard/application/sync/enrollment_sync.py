"""Sync engine for enrollments."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from blackboard.application.sync.base import BaseSyncEngine
from blackboard.domain.entities import Enrollment
from blackboard.domain.value_objects import EnrollmentId, StudentId, CourseId
from blackboard.infrastructure.providers.blackboard import BlackboardProvider


class EnrollmentSyncEngine(BaseSyncEngine[Enrollment, EnrollmentId]):
    """Sync enrollments between external system and Blackboard."""

    def __init__(self, provider: BlackboardProvider, external_data: List[Dict[str, Any]],
                 options=None):
        super().__init__(options)
        self.provider = provider
        self._external_data = external_data

    def get_external_data(self) -> List[Dict[str, Any]]:
        return self._external_data

    def get_blackboard_data(self) -> List[Enrollment]:
        all_enrollments = []
        for course in self.provider.courses.list_all():
            enrollments = self.provider.enrollments.list_by_course(course.id, active_only=self.options.active_only)
            all_enrollments.extend(enrollments)
        return all_enrollments

    def find_external_id(self, enrollment: Enrollment) -> str:
        return f"{enrollment.student_id}_{enrollment.course_id}"

    def get_external_id_from_data(self, data: Dict[str, Any]) -> str:
        return data.get('id') or f"{data['student_id']}_{data['course_id']}"

    def create_in_blackboard(self, data: Dict[str, Any]) -> Enrollment:
        enrollment = Enrollment(
            id=EnrollmentId(value=data.get('id') or f"{data['student_id']}_{data['course_id']}"),
            student_id=StudentId(value=data['student_id']),
            course_id=CourseId(value=data['course_id']),
            role=data.get('role', 'student'),
            active=data.get('active', True)
        )
        return self.provider.save(enrollment)

    def update_in_blackboard(self, enrollment: Enrollment, data: Dict[str, Any]) -> Enrollment:
        enrollment.role = data.get('role', enrollment.role)
        enrollment.active = data.get('active', enrollment.active)
        return self.provider.save(enrollment)

    def delete_in_blackboard(self, enrollment: Enrollment) -> None:
        self.provider.delete(enrollment.id)

    def compare(self, external_data: Dict[str, Any], enrollment: Enrollment) -> Optional[Dict[str, Any]]:
        changes = {}
        for key in ['role', 'active']:
            external_value = external_data.get(key)
            if external_value is not None:
                current_value = getattr(enrollment, key)
                if external_value != current_value:
                    changes[key] = external_value
        return changes if changes else None