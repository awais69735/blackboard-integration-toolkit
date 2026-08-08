"""Repository interfaces (ports) that abstract data access."""

from abc import ABC, abstractmethod
from typing import Iterable, Optional, List
from .entities import Student, Course, Enrollment, Assignment, Grade
from .value_objects import StudentId, CourseId, EnrollmentId, AssignmentId, GradeId


class StudentRepository(ABC):
    @abstractmethod
    def get(self, student_id: StudentId) -> Optional[Student]:
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[Student]:
        pass

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Student]:
        pass

    @abstractmethod
    def save(self, student: Student) -> Student:
        pass

    @abstractmethod
    def delete(self, student_id: StudentId) -> None:
        pass

class CourseRepository(ABC):
    """Port for course data operations."""

    @abstractmethod
    def get(self, course_id: CourseId) -> Optional[Course]:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Course]:
        pass

    @abstractmethod
    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Course]:
        pass

    @abstractmethod
    def save(self, course: Course) -> Course:
        pass

    @abstractmethod
    def delete(self, course_id: CourseId) -> None:
        pass


class EnrollmentRepository(ABC):
    """Port for enrollment data operations."""

    @abstractmethod
    def get(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        pass

    @abstractmethod
    def list_by_student(self, student_id: StudentId, *, active_only: bool = True) -> List[Enrollment]:
        pass

    @abstractmethod
    def list_by_course(self, course_id: CourseId, *, active_only: bool = True) -> List[Enrollment]:
        pass

    @abstractmethod
    def save(self, enrollment: Enrollment) -> Enrollment:
        pass

    @abstractmethod
    def delete(self, enrollment_id: EnrollmentId) -> None:
        pass


class AssignmentRepository(ABC):
    """Port for assignment data operations."""

    @abstractmethod
    def get(self, assignment_id: AssignmentId) -> Optional[Assignment]:
        pass

    @abstractmethod
    def list_by_course(self, course_id: CourseId) -> List[Assignment]:
        pass

    @abstractmethod
    def save(self, assignment: Assignment) -> Assignment:
        pass

    @abstractmethod
    def delete(self, assignment_id: AssignmentId) -> None:
        pass


class GradeRepository(ABC):
    """Port for grade data operations."""

    @abstractmethod
    def get(self, grade_id: GradeId) -> Optional[Grade]:
        pass

    @abstractmethod
    def list_by_student(self, student_id: StudentId) -> List[Grade]:
        pass

    @abstractmethod
    def list_by_assignment(self, assignment_id: AssignmentId) -> List[Grade]:
        pass

    @abstractmethod
    def save(self, grade: Grade) -> Grade:
        pass

    @abstractmethod
    def delete(self, grade_id: GradeId) -> None:
        pass