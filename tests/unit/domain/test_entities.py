"""Unit tests for domain entities."""

import pytest
from datetime import datetime
from blackboard.domain.entities import Student, Course, Enrollment, Assignment, Grade
from blackboard.domain.value_objects import (
    StudentId, CourseId, EnrollmentId, AssignmentId, GradeId, Email, DateRange
)


class TestStudent:
    def test_create_valid_student(self):
        student = Student(
            id=StudentId(value="123"),
            username="john.doe",
            email="john@example.com",   # fixed
            first_name="John",
            last_name="Doe"
        )
        assert student.full_name == "John Doe"
        assert student.username == "john.doe"

    def test_username_normalization(self):
        student = Student(
            id=StudentId(value="123"),
            username="  JaneDoe  ",
            email="jane@example.com",   # fixed
            first_name="Jane",
            last_name="Doe"
        )
        assert student.username == "janedoe"

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            Student(
                id=StudentId(value="123"),
                username="test",
                email="invalid-email",  # fixed - Pydantic will raise
                first_name="Test",
                last_name="User"
            )

class TestEnrollment:
    def test_drop_enrollment(self):
        enrollment = Enrollment(
            id=EnrollmentId(value="e1"),
            student_id=StudentId(value="s1"),
            course_id=CourseId(value="c1"),
            role="student"
        )
        assert enrollment.active is True
        enrollment.drop()
        assert enrollment.active is False
        assert enrollment.dropped_at is not None


class TestGrade:
    def test_grade_assignment(self):
        grade = Grade(
            id=GradeId(value="g1"),
            student_id=StudentId(value="s1"),
            assignment_id=AssignmentId(value="a1")
        )
        assert grade.is_graded() is False
        grade.grade(85.5, "Well done")
        assert grade.score == 85.5
        assert grade.feedback == "Well done"
        assert grade.graded_at is not None
        assert grade.updated_at is not None

    def test_grade_negative_score_raises(self):
        grade = Grade(
            id=GradeId(value="g2"),
            student_id=StudentId(value="s2"),
            assignment_id=AssignmentId(value="a2")
        )
        with pytest.raises(ValueError, match="Score cannot be negative"):
            grade.grade(-10)