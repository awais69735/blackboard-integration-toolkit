"""Integration tests for BlackboardProvider using the mock server."""

import pytest
from blackboard.domain.value_objects import StudentId, CourseId, EnrollmentId, AssignmentId
from blackboard.domain.entities import Student, Course, Enrollment, Assignment
from blackboard.exceptions.blackboard_errors import ResourceNotFoundError


class TestBlackboardProviderIntegration:

    def test_get_student(self, blackboard_provider):
        student = blackboard_provider.get(StudentId(value="s1"))
        assert student is not None
        assert student.username == "alice"
        assert student.email == "alice@example.com"

    def test_get_student_not_found(self, blackboard_provider):
        student = blackboard_provider.get(StudentId(value="s99"))
        assert student is None

    def test_get_by_username(self, blackboard_provider):
        student = blackboard_provider.get_by_username("bob")
        assert student is not None
        assert student.id.value == "s2"

    def test_list_students(self, blackboard_provider):
        students = blackboard_provider.list_students(limit=2)
        assert len(students) == 2
        assert students[0].username == "alice"

    def test_list_all_students(self, blackboard_provider):
        students = list(blackboard_provider.students.list_all())
        assert len(students) == 3

    def test_save_student_update(self, blackboard_provider):
        student = blackboard_provider.get(StudentId(value="s1"))
        student.first_name = "Alicia"
        updated = blackboard_provider.save(student)
        assert updated.first_name == "Alicia"
        fetched = blackboard_provider.get(StudentId(value="s1"))
        assert fetched.first_name == "Alicia"

    def test_delete_student(self, blackboard_provider):
        student = blackboard_provider.get(StudentId(value="s2"))
        assert student is not None
        blackboard_provider.delete(StudentId(value="s2"))
        assert blackboard_provider.get(StudentId(value="s2")) is None

    def test_get_course(self, blackboard_provider):
        course = blackboard_provider.get(CourseId(value="c1"))
        assert course is not None
        assert course.name == "Mathematics 101"

    def test_get_course_by_code(self, blackboard_provider):
        course = blackboard_provider.get_by_code("MATH101")
        assert course is not None
        assert course.id.value == "c1"

    def test_list_courses(self, blackboard_provider):
        courses = blackboard_provider.list_courses()
        assert len(courses) == 2

    def test_list_all_courses(self, blackboard_provider):
        courses = list(blackboard_provider.courses.list_all())
        assert len(courses) == 2

    def test_save_course_update(self, blackboard_provider):
        course = blackboard_provider.get(CourseId(value="c1"))
        course.name = "Advanced Mathematics 101"
        updated = blackboard_provider.save(course)
        assert updated.name == "Advanced Mathematics 101"
        fetched = blackboard_provider.get(CourseId(value="c1"))
        assert fetched.name == "Advanced Mathematics 101"

    def test_delete_course(self, blackboard_provider):
        course = blackboard_provider.get(CourseId(value="c2"))
        assert course is not None
        blackboard_provider.delete(CourseId(value="c2"))
        assert blackboard_provider.get(CourseId(value="c2")) is None

    def test_list_enrollments_by_course(self, blackboard_provider):
        enrollments = blackboard_provider.list_enrollments(CourseId(value="c1"))
        assert len(enrollments) == 2
        student_ids = {str(e.student_id) for e in enrollments}
        assert "s3" not in student_ids

    def test_list_enrollments_include_inactive(self, blackboard_provider):
        enrollments = blackboard_provider.list_enrollments(CourseId(value="c1"), active_only=False)
        assert len(enrollments) == 3

    def test_create_enrollment(self, blackboard_provider):
        enrollment = Enrollment(
            id=EnrollmentId(value="s3_c2"),
            student_id=StudentId(value="s3"),
            course_id=CourseId(value="c2"),
            role="student"
        )
        created = blackboard_provider.save(enrollment)
        assert created is not None
        enrollments = blackboard_provider.list_enrollments(CourseId(value="c2"), active_only=False)
        assert any(e.student_id.value == "s3" for e in enrollments)

    def test_delete_enrollment(self, blackboard_provider):
        # Ensure enrollment exists before deletion
        enrollments_before = blackboard_provider.list_enrollments(CourseId(value="c1"), active_only=False)
        assert any(e.student_id.value == "s3" for e in enrollments_before)

        enrollment_id = EnrollmentId(value="s3_c1")
        blackboard_provider.delete(enrollment_id)

        enrollments_after = blackboard_provider.list_enrollments(CourseId(value="c1"), active_only=False)
        assert not any(e.student_id.value == "s3" for e in enrollments_after)

    def test_list_assignments(self, blackboard_provider):
        assignments = blackboard_provider.assignments.list_by_course(CourseId(value="c1"))
        assert len(assignments) == 2
        names = {a.name for a in assignments}
        assert names == {"Homework 1", "Midterm Exam"}

    def test_create_assignment(self, blackboard_provider):
        assignment = Assignment(
            id=None,  # will be generated
            course_id=CourseId(value="c1"),
            name="Quiz 1",
            points_possible=50.0
        )
        created = blackboard_provider.save(assignment)
        assert created.id is not None
        assignments = blackboard_provider.assignments.list_by_course(CourseId(value="c1"))
        assert any(a.name == "Quiz 1" for a in assignments)

    def test_update_assignment(self, blackboard_provider):
        assignments = blackboard_provider.assignments.list_by_course(CourseId(value="c1"))
        assignment = next(a for a in assignments if a.name == "Homework 1")
        assignment.name = "Homework 1 (Updated)"
        updated = blackboard_provider.save(assignment)
        assert updated.name == "Homework 1 (Updated)"
        assignments_after = blackboard_provider.assignments.list_by_course(CourseId(value="c1"))
        updated_assignment = next(a for a in assignments_after if a.id == assignment.id)
        assert updated_assignment.name == "Homework 1 (Updated)"