"""Sync engine for courses."""

from typing import List, Dict, Any, Optional
from blackboard.application.sync.base import BaseSyncEngine
from blackboard.domain.entities import Course
from blackboard.domain.value_objects import CourseId
from blackboard.infrastructure.providers.blackboard import BlackboardProvider


class CourseSyncEngine(BaseSyncEngine[Course, CourseId]):
    """Sync courses between external system and Blackboard."""

    def __init__(self, provider: BlackboardProvider, external_data: List[Dict[str, Any]],
                 options=None):
        super().__init__(options)
        self.provider = provider
        self._external_data = external_data

    def get_external_data(self) -> List[Dict[str, Any]]:
        return self._external_data

    def get_blackboard_data(self) -> List[Course]:
        return list(self.provider.courses.list_all())

    def find_external_id(self, course: Course) -> str:
        return course.id.value

    def get_external_id_from_data(self, data: Dict[str, Any]) -> str:
        return data.get('id')

    def create_in_blackboard(self, data: Dict[str, Any]) -> Course:
        course = Course(
            id=CourseId(value=data.get('id')),
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description'),
            term=data.get('term'),
            active=data.get('active', True)
        )
        return self.provider.save(course)

    def update_in_blackboard(self, course: Course, data: Dict[str, Any]) -> Course:
        course.name = data.get('name', course.name)
        course.code = data.get('code', course.code)
        course.description = data.get('description', course.description)
        course.term = data.get('term', course.term)
        course.active = data.get('active', course.active)
        return self.provider.save(course)

    def delete_in_blackboard(self, course: Course) -> None:
        self.provider.delete(course.id)

    def compare(self, external_data: Dict[str, Any], course: Course) -> Optional[Dict[str, Any]]:
        changes = {}
        for key in ['name', 'code', 'description', 'term', 'active']:
            external_value = external_data.get(key)
            if external_value is not None:
                current_value = getattr(course, key)
                if external_value != current_value:
                    changes[key] = external_value
        return changes if changes else None