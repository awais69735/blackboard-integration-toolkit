"""Sync engine for grades."""

from typing import List, Dict, Any, Optional
from blackboard.application.sync.base import BaseSyncEngine
from blackboard.domain.entities import Grade
from blackboard.domain.value_objects import GradeId, StudentId, AssignmentId
from blackboard.infrastructure.providers.blackboard import BlackboardProvider


class GradeSyncEngine(BaseSyncEngine[Grade, GradeId]):
    """Sync grades between external system and Blackboard."""

    def __init__(self, provider: BlackboardProvider, external_data: List[Dict[str, Any]],
                 assignment_id: str = None, course_id: str = None, options=None):
        super().__init__(options)
        self.provider = provider
        self._external_data = external_data
        self.assignment_id = assignment_id
        self.course_id = course_id

    def get_external_data(self) -> List[Dict[str, Any]]:
        return self._external_data

    def get_blackboard_data(self) -> List[Grade]:
        # Stub: in production, implement fetching grades from gradebook columns
        return []

    def find_external_id(self, grade: Grade) -> str:
        return f"{grade.student_id}_{grade.assignment_id}"

    def get_external_id_from_data(self, data: Dict[str, Any]) -> str:
        return data.get('id') or f"{data['student_id']}_{data['assignment_id']}"

    def create_in_blackboard(self, data: Dict[str, Any]) -> Grade:
        grade = Grade(
            id=GradeId(value=data.get('id') or f"{data['student_id']}_{data['assignment_id']}"),
            student_id=StudentId(value=data['student_id']),
            assignment_id=AssignmentId(value=data['assignment_id']),
            score=data.get('score'),
            feedback=data.get('feedback')
        )
        return self.provider.save(grade)

    def update_in_blackboard(self, grade: Grade, data: Dict[str, Any]) -> Grade:
        grade.score = data.get('score', grade.score)
        grade.feedback = data.get('feedback', grade.feedback)
        return self.provider.save(grade)

    def delete_in_blackboard(self, grade: Grade) -> None:
        self.provider.delete(grade.id)

    def compare(self, external_data: Dict[str, Any], grade: Grade) -> Optional[Dict[str, Any]]:
        changes = {}
        for key in ['score', 'feedback']:
            external_value = external_data.get(key)
            if external_value is not None:
                current_value = getattr(grade, key)
                if external_value != current_value:
                    changes[key] = external_value
        return changes if changes else None