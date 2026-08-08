"""In‑memory implementations of repositories for testing and prototyping."""

from typing import List, Optional, Dict, Any
from uuid import uuid4
from blackboard.domain.entities import Student, Course, Enrollment, Assignment, Grade
from blackboard.domain.value_objects import (
    StudentId, CourseId, EnrollmentId, AssignmentId, GradeId
)
from blackboard.domain.interfaces import (
    StudentRepository, CourseRepository, EnrollmentRepository,
    AssignmentRepository, GradeRepository
)


class InMemoryStudentRepository(StudentRepository):
    """In‑memory storage for students."""

    def __init__(self):
        self._store: Dict[str, Student] = {}

    def get(self, student_id: StudentId) -> Optional[Student]:
        return self._store.get(str(student_id))

    def get_by_username(self, username: str) -> Optional[Student]:
        for student in self._store.values():
            if student.username == username:
                return student
        return None

    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Student]:
        results = list(self._store.values())
        # Simple filtering (can be extended)
        if filters.get("active") is not None:
            results = [s for s in results if s.active == filters["active"]]
        return results[offset:offset + limit]

    def save(self, student: Student) -> Student:
        self._store[str(student.id)] = student
        return student

    def delete(self, student_id: StudentId) -> None:
        self._store.pop(str(student_id), None)


class InMemoryCourseRepository(CourseRepository):
    def __init__(self):
        self._store: Dict[str, Course] = {}

    def get(self, course_id: CourseId) -> Optional[Course]:
        return self._store.get(str(course_id))

    def get_by_code(self, code: str) -> Optional[Course]:
        for course in self._store.values():
            if course.code == code:
                return course
        return None

    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Course]:
        results = list(self._store.values())
        if filters.get("active") is not None:
            results = [c for c in results if c.active == filters["active"]]
        return results[offset:offset + limit]

    def save(self, course: Course) -> Course:
        self._store[str(course.id)] = course
        return course

    def delete(self, course_id: CourseId) -> None:
        self._store.pop(str(course_id), None)


# Similarly, implement InMemoryEnrollmentRepository, InMemoryAssignmentRepository, InMemoryGradeRepository
# (We can keep them concise; for brevity, we'll include them but with minimal implementation.)

class InMemoryEnrollmentRepository(EnrollmentRepository):
    def __init__(self):
        self._store: Dict[str, Enrollment] = {}

    def get(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        return self._store.get(str(enrollment_id))

    def list_by_student(self, student_id: StudentId, *, active_only: bool = True) -> List[Enrollment]:
        results = [e for e in self._store.values() if e.student_id == student_id]
        if active_only:
            results = [e for e in results if e.active]
        return results

    def list_by_course(self, course_id: CourseId, *, active_only: bool = True) -> List[Enrollment]:
        results = [e for e in self._store.values() if e.course_id == course_id]
        if active_only:
            results = [e for e in results if e.active]
        return results

    def save(self, enrollment: Enrollment) -> Enrollment:
        self._store[str(enrollment.id)] = enrollment
        return enrollment

    def delete(self, enrollment_id: EnrollmentId) -> None:
        self._store.pop(str(enrollment_id), None)


class InMemoryAssignmentRepository(AssignmentRepository):
    def __init__(self):
        self._store: Dict[str, Assignment] = {}

    def get(self, assignment_id: AssignmentId) -> Optional[Assignment]:
        return self._store.get(str(assignment_id))

    def list_by_course(self, course_id: CourseId) -> List[Assignment]:
        return [a for a in self._store.values() if a.course_id == course_id]

    def save(self, assignment: Assignment) -> Assignment:
        self._store[str(assignment.id)] = assignment
        return assignment

    def delete(self, assignment_id: AssignmentId) -> None:
        self._store.pop(str(assignment_id), None)


class InMemoryGradeRepository(GradeRepository):
    def __init__(self):
        self._store: Dict[str, Grade] = {}

    def get(self, grade_id: GradeId) -> Optional[Grade]:
        return self._store.get(str(grade_id))

    def list_by_student(self, student_id: StudentId) -> List[Grade]:
        return [g for g in self._store.values() if g.student_id == student_id]

    def list_by_assignment(self, assignment_id: AssignmentId) -> List[Grade]:
        return [g for g in self._store.values() if g.assignment_id == assignment_id]

    def save(self, grade: Grade) -> Grade:
        self._store[str(grade.id)] = grade
        return grade

    def delete(self, grade_id: GradeId) -> None:
        self._store.pop(str(grade_id), None)