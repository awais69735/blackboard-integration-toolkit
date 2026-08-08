"""Tests for BlackboardProvider using the mock server."""

import pytest
from blackboard.domain.value_objects import StudentId, CourseId


def test_get_student(blackboard_provider):
    student = blackboard_provider.get(StudentId(value="s1"))
    assert student is not None
    assert student.username == "alice"


def test_get_student_not_found(blackboard_provider):
    student = blackboard_provider.get(StudentId(value="s99"))
    assert student is None


def test_list_students(blackboard_provider):
    students = blackboard_provider.list_students(limit=2)
    assert len(students) == 2
    assert students[0].username == "alice"


def test_get_course(blackboard_provider):
    course = blackboard_provider.get(CourseId(value="c1"))
    assert course is not None
    assert course.name == "Mathematics 101"


def test_list_enrollments(blackboard_provider):
    enrollments = blackboard_provider.list_enrollments(CourseId(value="c1"))
    assert len(enrollments) == 2
    assert str(enrollments[0].student_id) == "s1"