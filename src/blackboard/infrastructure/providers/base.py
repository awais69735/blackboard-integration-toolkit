"""Abstract provider base class (kept for future extension)."""

from abc import ABC, abstractmethod
from blackboard.domain.entities import Student, Course, Enrollment
from typing import Iterable, Optional


class LMSProvider(ABC):
    @abstractmethod
    def get_student(self, student_id: str) -> Optional[Student]:
        pass

    @abstractmethod
    def list_students(self, **filters) -> Iterable[Student]:
        pass