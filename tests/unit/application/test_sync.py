"""Unit tests for sync engines."""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone

from blackboard.application.sync.student_sync import StudentSyncEngine
from blackboard.application.dto import SyncOptions, SyncStatus
from blackboard.domain.entities import Student
from blackboard.domain.value_objects import StudentId


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