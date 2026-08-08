"""High-level facade for the toolkit."""

from typing import Optional, List
from blackboard.domain.entities import Student, Course
from blackboard.infrastructure.providers import BlackboardProvider


class LMSService:
    """Facade providing a unified API for LMS operations."""

    def __init__(self, provider: BlackboardProvider):
        self._provider = provider

    def get_student(self, student_id: str) -> Optional[Student]:
        return self._provider.get(student_id)

    def list_students(self, **filters) -> List[Student]:
        return self._provider.list(**filters)

    def get_course(self, course_id: str) -> Optional[Course]:
        return self._provider.get(course_id)

    # Additional methods ...