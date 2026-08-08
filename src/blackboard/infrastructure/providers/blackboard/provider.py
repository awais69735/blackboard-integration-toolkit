"""Blackboard adapters implementing repository interfaces using composition."""

from functools import singledispatchmethod
from typing import List, Optional, Iterable
from datetime import datetime, timezone

from blackboard.domain.entities import Student, Course, Enrollment, Assignment, Grade
from blackboard.domain.value_objects import StudentId, CourseId, EnrollmentId, AssignmentId, GradeId
from blackboard.domain.interfaces import (
    StudentRepository, CourseRepository, EnrollmentRepository,
    AssignmentRepository, GradeRepository
)
from blackboard.infrastructure.http import HTTPClient, PageIterator
from blackboard.infrastructure.logging import get_logger
from blackboard.exceptions import ResourceNotFoundError
from .resources import USERS, COURSES, ENROLLMENTS, ASSIGNMENTS, CREATE_ASSIGNMENT, GRADEBOOK_COLUMNS
from .mapper import BlackboardResourceMapper

logger = get_logger(__name__)


# ---------- Individual repository implementations ----------
class BlackboardStudentRepository(StudentRepository):
    def __init__(self, http_client: HTTPClient, mapper: BlackboardResourceMapper):
        self._http = http_client
        self._mapper = mapper

    def get(self, student_id: StudentId) -> Optional[Student]:
        url = f"{USERS}/{student_id}"
        try:
            resp = self._http.get(url)
            return self._mapper.to_student(resp.json())
        except ResourceNotFoundError:
            return None

    def get_by_username(self, username: str) -> Optional[Student]:
        resp = self._http.get(USERS, params={"userName": username})
        data = resp.json()
        results = data.get("results", [])
        return self._mapper.to_student(results[0]) if results else None

    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Student]:
        params = {"limit": limit, "offset": offset}
        params.update(filters)
        resp = self._http.get(USERS, params=params)
        data = resp.json()
        return [self._mapper.to_student(item) for item in data.get("results", [])]

    def list_all(self, **filters) -> Iterable[Student]:
        def fetch_page(limit, offset, **filters):
            resp = self._http.get(USERS, params={"limit": limit, "offset": offset, **filters})
            data = resp.json()
            return data.get("results", []), data.get("totalCount", 0)
        pager = PageIterator(fetch_page, **filters)
        for item in pager:
            yield self._mapper.to_student(item)

    def save(self, student: Student) -> Student:
        # Try to get the student first
        existing = self.get(student.id)
        if existing:
            # Update
            url = f"{USERS}/{student.id}"
            payload = {
                "userName": student.username,
                "email": str(student.email),
                "firstName": student.first_name,
                "lastName": student.last_name,
                "active": student.active,
            }
            resp = self._http.patch(url, json=payload)
        else:
            # Create
            url = USERS  # POST to collection
            payload = {
                "userName": student.username,
                "email": str(student.email),
                "firstName": student.first_name,
                "lastName": student.last_name,
                "active": student.active,
            }
            resp = self._http.post(url, json=payload)
        return self._mapper.to_student(resp.json())

    def delete(self, student_id: StudentId) -> None:
        url = f"{USERS}/{student_id}"
        try:
            self._http.delete(url)
        except ResourceNotFoundError:
            pass


class BlackboardCourseRepository(CourseRepository):
    def __init__(self, http_client: HTTPClient, mapper: BlackboardResourceMapper):
        self._http = http_client
        self._mapper = mapper

    def get(self, course_id: CourseId) -> Optional[Course]:
        url = f"{COURSES}/{course_id}"
        try:
            resp = self._http.get(url)
            return self._mapper.to_course(resp.json())
        except ResourceNotFoundError:
            return None

    def get_by_code(self, code: str) -> Optional[Course]:
        resp = self._http.get(COURSES, params={"courseId": code})
        data = resp.json()
        results = data.get("results", [])
        return self._mapper.to_course(results[0]) if results else None

    def list(self, *, limit: int = 100, offset: int = 0, **filters) -> List[Course]:
        params = {"limit": limit, "offset": offset}
        params.update(filters)
        resp = self._http.get(COURSES, params=params)
        data = resp.json()
        return [self._mapper.to_course(item) for item in data.get("results", [])]

    def list_all(self, **filters) -> Iterable[Course]:
        def fetch_page(limit, offset, **filters):
            resp = self._http.get(COURSES, params={"limit": limit, "offset": offset, **filters})
            data = resp.json()
            return data.get("results", []), data.get("totalCount", 0)
        pager = PageIterator(fetch_page, **filters)
        for item in pager:
            yield self._mapper.to_course(item)

    def save(self, course: Course) -> Course:
        # Try to get the course first
        existing = self.get(course.id)
        if existing:
            # Update
            url = f"{COURSES}/{course.id}"
            payload = {
                "name": course.name,
                "courseId": course.code,
                "description": course.description,
                "available": course.active,
            }
            resp = self._http.patch(url, json=payload)
        else:
            # Create
            url = COURSES
            payload = {
                "name": course.name,
                "courseId": course.code,
                "description": course.description,
                "available": course.active,
            }
            resp = self._http.post(url, json=payload)
        return self._mapper.to_course(resp.json())

    
    def delete(self, course_id: CourseId) -> None:
        url = f"{COURSES}/{course_id}"
        try:
            self._http.delete(url)
        except ResourceNotFoundError:
            pass


class BlackboardEnrollmentRepository(EnrollmentRepository):
    def __init__(self, http_client: HTTPClient, mapper: BlackboardResourceMapper):
        self._http = http_client
        self._mapper = mapper

    def get(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        raise NotImplementedError("GET enrollment by ID not directly supported")

    def list_by_student(self, student_id: StudentId, *, active_only: bool = True) -> List[Enrollment]:
        resp = self._http.get(COURSES, params={"userId": str(student_id)})
        data = resp.json()
        results = data.get("results", [])
        enrollments = []
        for course_data in results:
            enroll = Enrollment(
                id=EnrollmentId(value=f"{student_id}_{course_data['id']}"),
                student_id=student_id,
                course_id=CourseId(value=course_data["id"]),
                role="student",
                enrolled_at=datetime.now(timezone.utc),
                active=True,
            )
            if active_only and not enroll.active:
                continue
            enrollments.append(enroll)
        return enrollments

    def list_by_course(self, course_id: CourseId, *, active_only: bool = True) -> List[Enrollment]:
        url = ENROLLMENTS.format(course_id=course_id)
        resp = self._http.get(url)
        data = resp.json()
        results = data.get("results", [])
        enrollments = []
        for item in results:
            enroll = self._mapper.to_enrollment(item, str(course_id))
            if active_only and not enroll.active:
                continue
            enrollments.append(enroll)
        return enrollments

    def save(self, enrollment: Enrollment) -> Enrollment:
        url = ENROLLMENTS.format(course_id=enrollment.course_id)
        payload = {
            "userId": str(enrollment.student_id),
            "role": enrollment.role,
        }
        resp = self._http.post(url, json=payload)
        data = resp.json()
        if "id" not in data:
            data["id"] = f"{enrollment.student_id}_{enrollment.course_id}"
        return self._mapper.to_enrollment(data, str(enrollment.course_id))

    def delete(self, enrollment_id: EnrollmentId) -> None:
        parts = str(enrollment_id).split("_")
        if len(parts) != 2:
            raise ValueError("Invalid enrollment_id format; expected 'studentId_courseId'")
        student_id, course_id = parts
        url = ENROLLMENTS.format(course_id=course_id)
        delete_url = f"{url}/{student_id}"
        try:
            self._http.delete(delete_url)
        except ResourceNotFoundError:
            pass


class BlackboardAssignmentRepository(AssignmentRepository):
    def __init__(self, http_client: HTTPClient, mapper: BlackboardResourceMapper):
        self._http = http_client
        self._mapper = mapper

    def get(self, assignment_id: AssignmentId) -> Optional[Assignment]:
        raise NotImplementedError("GET assignment by ID requires course_id")

    def list_by_course(self, course_id: CourseId) -> List[Assignment]:
        url = ASSIGNMENTS.format(course_id=course_id)
        resp = self._http.get(url)
        data = resp.json()
        return [self._mapper.to_assignment(item) for item in data.get("results", [])]

    def save(self, assignment: Assignment) -> Assignment:
        if assignment.id and assignment.id.value:
            # Update existing assignment
            url = f"{ASSIGNMENTS.format(course_id=assignment.course_id)}/{assignment.id}"
            payload = {
                "name": assignment.name,
                "description": assignment.description,
                "dueDate": assignment.due_date.isoformat() if assignment.due_date else None,
                "points": {"possible": assignment.points_possible},
            }
            resp = self._http.patch(url, json=payload)
        else:
            # Create new assignment using the new createAssignment endpoint
            url = CREATE_ASSIGNMENT.format(course_id=assignment.course_id)
            payload = {
                "name": assignment.name,
                "description": assignment.description,
                "dueDate": assignment.due_date.isoformat() if assignment.due_date else None,
                "points": {"possible": assignment.points_possible},
            }
            resp = self._http.post(url, json=payload)
        data = resp.json()
        return self._mapper.to_assignment(data)

    def delete(self, assignment_id: AssignmentId) -> None:
        raise NotImplementedError("Delete assignment requires course_id")


# ---------- Gradebook stub ----------
class BlackboardGradeRepository(GradeRepository):
    def __init__(self, http_client: HTTPClient, mapper: BlackboardResourceMapper):
        self._http = http_client
        self._mapper = mapper

    def get(self, grade_id: GradeId) -> Optional[Grade]:
        raise NotImplementedError("GET grade by ID not directly supported")

    def list_by_student(self, student_id: StudentId) -> List[Grade]:
        raise NotImplementedError("List grades by student requires course iteration")

    def list_by_assignment(self, assignment_id: AssignmentId) -> List[Grade]:
        raise NotImplementedError("List grades by assignment requires course_id")

    def save(self, grade: Grade) -> Grade:
        raise NotImplementedError("Save grade not yet implemented")

    def delete(self, grade_id: GradeId) -> None:
        raise NotImplementedError("Delete grade not implemented")


# ---------- Main facade ----------
class BlackboardProvider:
    """Facade that composes all repository implementations."""

    def __init__(self, http_client: HTTPClient):
        self._http = http_client
        self._mapper = BlackboardResourceMapper()

        self.students = BlackboardStudentRepository(http_client, self._mapper)
        self.courses = BlackboardCourseRepository(http_client, self._mapper)
        self.enrollments = BlackboardEnrollmentRepository(http_client, self._mapper)
        self.assignments = BlackboardAssignmentRepository(http_client, self._mapper)
        self.grades = BlackboardGradeRepository(http_client, self._mapper)

    # Convenience methods that dispatch to the appropriate repository
    @singledispatchmethod
    def get(self, identifier):
        raise NotImplementedError(f"get not implemented for {type(identifier)}")

    @get.register(StudentId)
    def _get_student(self, student_id: StudentId) -> Optional[Student]:
        return self.students.get(student_id)

    @get.register(CourseId)
    def _get_course(self, course_id: CourseId) -> Optional[Course]:
        return self.courses.get(course_id)

    @get.register(EnrollmentId)
    def _get_enrollment(self, enrollment_id: EnrollmentId) -> Optional[Enrollment]:
        return self.enrollments.get(enrollment_id)

    @get.register(AssignmentId)
    def _get_assignment(self, assignment_id: AssignmentId) -> Optional[Assignment]:
        return self.assignments.get(assignment_id)

    @get.register(GradeId)
    def _get_grade(self, grade_id: GradeId) -> Optional[Grade]:
        return self.grades.get(grade_id)

    # Additional convenience methods for common operations
    def get_by_username(self, username: str) -> Optional[Student]:
        return self.students.get_by_username(username)

    def get_by_code(self, code: str) -> Optional[Course]:
        return self.courses.get_by_code(code)

    def list_students(self, **filters) -> List[Student]:
        return self.students.list(**filters)

    def list_courses(self, **filters) -> List[Course]:
        return self.courses.list(**filters)

    def list_enrollments(self, course_id: CourseId, *, active_only: bool = True) -> List[Enrollment]:
        return self.enrollments.list_by_course(course_id, active_only=active_only)

    def list_assignments(self, course_id: CourseId) -> List[Assignment]:
        return self.assignments.list_by_course(course_id)

    # Save and delete also dispatch
    @singledispatchmethod
    def save(self, entity):
        raise NotImplementedError(f"save not implemented for {type(entity)}")

    @save.register(Student)
    def _save_student(self, student: Student) -> Student:
        return self.students.save(student)

    @save.register(Course)
    def _save_course(self, course: Course) -> Course:
        return self.courses.save(course)

    @save.register(Enrollment)
    def _save_enrollment(self, enrollment: Enrollment) -> Enrollment:
        return self.enrollments.save(enrollment)

    @save.register(Assignment)
    def _save_assignment(self, assignment: Assignment) -> Assignment:
        return self.assignments.save(assignment)

    @save.register(Grade)
    def _save_grade(self, grade: Grade) -> Grade:
        return self.grades.save(grade)

    @singledispatchmethod
    def delete(self, identifier):
        raise NotImplementedError(f"delete not implemented for {type(identifier)}")

    @delete.register(StudentId)
    def _delete_student(self, student_id: StudentId) -> None:
        self.students.delete(student_id)

    @delete.register(CourseId)
    def _delete_course(self, course_id: CourseId) -> None:
        self.courses.delete(course_id)

    @delete.register(EnrollmentId)
    def _delete_enrollment(self, enrollment_id: EnrollmentId) -> None:
        self.enrollments.delete(enrollment_id)

    @delete.register(AssignmentId)
    def _delete_assignment(self, assignment_id: AssignmentId) -> None:
        self.assignments.delete(assignment_id)

    @delete.register(GradeId)
    def _delete_grade(self, grade_id: GradeId) -> None:
        self.grades.delete(grade_id)