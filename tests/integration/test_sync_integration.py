"""Integration tests for sync engines using the mock server."""

import pytest
from blackboard.application.services.sync_service import SyncService
from blackboard.application.dto import SyncOptions, SyncStatus
from blackboard.domain.value_objects import CourseId


class TestSyncIntegration:

    def test_sync_students_creates_and_updates(self, blackboard_provider):
        service = SyncService(blackboard_provider)

        external_students = [
            {"id": "s99", "username": "new_student", "email": "new@example.com",
             "first_name": "New", "last_name": "User", "active": True},
            {"id": "s1", "username": "alice_updated", "email": "alice@example.com",
             "first_name": "Alice", "last_name": "Smith", "active": True},
        ]

        result = service.sync_students(external_students, SyncOptions(dry_run=False))
        assert result.status == SyncStatus.SUCCESS
        assert result.created == 1
        assert result.updated == 1

    def test_sync_courses_creates_and_updates(self, blackboard_provider):
        service = SyncService(blackboard_provider)

        # Ensure the new course doesn't exist before the test
        try:
            blackboard_provider.delete(CourseId(value="c_new_course"))
        except Exception:
            pass  # ignore if it doesn't exist

        external_courses = [
            {"id": "c_new_course", "name": "New Course", "code": "NEW101", "active": True},
            {"id": "c1", "name": "Updated Math", "code": "MATH101", "active": True},
        ]

        result = service.sync_courses(external_courses, SyncOptions(dry_run=False))
        assert result.status == SyncStatus.SUCCESS
        assert result.created == 1
        assert result.updated == 1

    def test_sync_enrollments(self, blackboard_provider):
        service = SyncService(blackboard_provider)

        external_enrollments = [
            {"student_id": "s1", "course_id": "c2", "role": "student", "active": True},
        ]

        result = service.sync_enrollments(external_enrollments, SyncOptions(dry_run=False))
        assert result.status == SyncStatus.SUCCESS
        assert result.created >= 0