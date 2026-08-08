"""Unit tests for all sync engines."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from blackboard.application.sync.student_sync import StudentSyncEngine
from blackboard.application.sync.course_sync import CourseSyncEngine
from blackboard.application.sync.enrollment_sync import EnrollmentSyncEngine
from blackboard.application.sync.grade_sync import GradeSyncEngine
from blackboard.application.dto import SyncOptions, SyncStatus
from blackboard.domain.entities import Student, Course, Enrollment, Grade
from blackboard.domain.value_objects import StudentId, CourseId, EnrollmentId, AssignmentId, GradeId


class TestStudentSyncEngine:

    def test_sync_creates_new_students(self):
        provider = Mock()
        external_data = [
            {"id": "ext1", "username": "john", "email": "john@example.com",
             "first_name": "John", "last_name": "Doe"}
        ]
        provider.students.list_all.return_value = []
        options = SyncOptions()
        engine = StudentSyncEngine(provider, external_data, options)
        engine.create_in_blackboard = Mock(return_value=Student(
            id=StudentId(value="ext1"), username="john", email="john@example.com",
            first_name="John", last_name="Doe"
        ))
        result = engine.sync()
        assert result.created == 1
        assert result.status == SyncStatus.SUCCESS

    def test_sync_updates_existing_students(self):
        provider = Mock()
        existing_student = Student(
            id=StudentId(value="ext1"), username="john", email="john@example.com",
            first_name="John", last_name="Doe", active=True
        )
        provider.students.list_all.return_value = [existing_student]
        external_data = [
            {"id": "ext1", "username": "john_updated", "email": "john@example.com",
             "first_name": "John", "last_name": "Doe", "active": True}
        ]
        options = SyncOptions()
        engine = StudentSyncEngine(provider, external_data, options)
        engine.update_in_blackboard = Mock(return_value=existing_student)
        result = engine.sync()
        assert result.updated == 1
        assert result.status == SyncStatus.SUCCESS

    def test_sync_handles_dry_run(self):
        provider = Mock()
        external_data = [{"id": "ext1", "username": "john"}]
        provider.students.list_all.return_value = []
        options = SyncOptions(dry_run=True)
        engine = StudentSyncEngine(provider, external_data, options)
        result = engine.sync()
        assert result.status == SyncStatus.DRY_RUN


class TestCourseSyncEngine:

    def test_sync_creates_new_courses(self):
        provider = Mock()
        external_data = [{"id": "c1", "name": "Math 101", "code": "MATH101"}]
        provider.courses.list_all.return_value = []
        options = SyncOptions()
        engine = CourseSyncEngine(provider, external_data, options)
        engine.create_in_blackboard = Mock(return_value=Course(
            id=CourseId(value="c1"), name="Math 101", code="MATH101"
        ))
        result = engine.sync()
        assert result.created == 1
        assert result.status == SyncStatus.SUCCESS


class TestEnrollmentSyncEngine:

    def test_sync_creates_new_enrollments(self):
        provider = Mock()
        external_data = [
            {"id": "s1_c1", "student_id": "s1", "course_id": "c1", "role": "student"}
        ]
        provider.courses.list_all.return_value = [Course(
            id=CourseId(value="c1"), name="Math", code="MATH"
        )]
        provider.enrollments.list_by_course.return_value = []
        options = SyncOptions()
        engine = EnrollmentSyncEngine(provider, external_data, options)
        engine.create_in_blackboard = Mock(return_value=Enrollment(
            id=EnrollmentId(value="s1_c1"), student_id=StudentId(value="s1"),
            course_id=CourseId(value="c1"), role="student"
        ))
        result = engine.sync()
        assert result.created == 1
   
class TestGradeSyncEngine:

    def test_sync_creates_new_grades(self):
        provider = Mock()
        external_data = [
            {"id": "s1_a1", "student_id": "s1", "assignment_id": "a1", "score": 85.0}
        ]
        with patch.object(GradeSyncEngine, 'get_blackboard_data', return_value=[]):
            options = SyncOptions()
            engine = GradeSyncEngine(provider, external_data, assignment_id="a1", options=options)
            engine.create_in_blackboard = Mock(return_value=Grade(
                id=GradeId(value="s1_a1"), student_id=StudentId(value="s1"),
                assignment_id=AssignmentId(value="a1"), score=85.0
            ))
            result = engine.sync()
            assert result.created == 1