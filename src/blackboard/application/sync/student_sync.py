"""Sync engine for students."""

from typing import List, Dict, Any, Optional
from blackboard.application.sync.base import BaseSyncEngine
from blackboard.domain.entities import Student
from blackboard.domain.value_objects import StudentId
from blackboard.infrastructure.providers.blackboard import BlackboardProvider


class StudentSyncEngine(BaseSyncEngine[Student, StudentId]):
    """Sync students between external system and Blackboard."""

    def __init__(self, provider: BlackboardProvider, external_data: List[Dict[str, Any]],
                 options=None):
        super().__init__(options)
        self.provider = provider
        self._external_data = external_data

    def get_external_data(self) -> List[Dict[str, Any]]:
        return self._external_data

    def get_blackboard_data(self) -> List[Student]:
        return list(self.provider.students.list_all())

    def find_external_id(self, student: Student) -> str:
        return student.id.value

    def get_external_id_from_data(self, data: Dict[str, Any]) -> str:
        return data.get('id')

    def create_in_blackboard(self, data: Dict[str, Any]) -> Student:
        student = Student(
            id=StudentId(value=data.get('id')),
            username=data.get('username'),
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            active=data.get('active', True)
        )
        return self.provider.save(student)

    def update_in_blackboard(self, student: Student, data: Dict[str, Any]) -> Student:
        student.username = data.get('username', student.username)
        student.email = data.get('email', student.email)
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.active = data.get('active', student.active)
        return self.provider.save(student)

    def delete_in_blackboard(self, student: Student) -> None:
        self.provider.delete(student.id)

    def compare(self, external_data: Dict[str, Any], student: Student) -> Optional[Dict[str, Any]]:
        changes = {}
        for key in ['username', 'email', 'first_name', 'last_name', 'active']:
            external_value = external_data.get(key)
            if external_value is not None:
                current_value = getattr(student, key)
                if external_value != current_value:
                    changes[key] = external_value
        return changes if changes else None