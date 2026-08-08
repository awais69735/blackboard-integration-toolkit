"""Mapper between Blackboard API JSON and domain entities."""

from typing import Dict, Any, Optional
from datetime import datetime
from blackboard.domain.entities import Student, Course, Enrollment, Assignment, Grade
from blackboard.domain.value_objects import (
    StudentId, CourseId, EnrollmentId, AssignmentId, GradeId, DateRange
)


class BlackboardResourceMapper:
    @staticmethod
    def to_student(data: Dict[str, Any]) -> Student:
        return Student(
            id=StudentId(value=data["id"]),
            username=data["userName"],
            email=data.get("email", f"{data['userName']}@example.com"),
            first_name=data.get("firstName", ""),
            last_name=data.get("lastName", ""),
            active=data.get("active", True),
            created_at=datetime.fromisoformat(data["created"]) if data.get("created") else None,
            updated_at=datetime.fromisoformat(data["modified"]) if data.get("modified") else None,
        )

    @staticmethod
    def to_course(data: Dict[str, Any]) -> Course:
        # v3 response may include additional fields, but we map the core ones
        return Course(
            id=CourseId(value=data["id"]),
            name=data.get("name", ""),
            code=data.get("courseId", ""),
            description=data.get("description"),
            term=data.get("term", {}).get("name") if data.get("term") else None,
            date_range=DateRange(
                start=datetime.fromisoformat(data["startDate"]) if data.get("startDate") else None,
                end=datetime.fromisoformat(data["endDate"]) if data.get("endDate") else None,
            ),
            active=data.get("available", True),
            created_at=datetime.fromisoformat(data["created"]) if data.get("created") else None,
            updated_at=datetime.fromisoformat(data["modified"]) if data.get("modified") else None,
        )

    @staticmethod
    def to_enrollment(data: Dict[str, Any], course_id: str = None) -> Enrollment:
        enrollment_id = data.get("id") or f"{data.get('userId')}_{course_id or data.get('courseId')}"
        return Enrollment(
            id=EnrollmentId(value=enrollment_id),
            student_id=StudentId(value=data["userId"]),
            course_id=CourseId(value=data.get("courseId") or course_id or ""),
            role=data.get("role", "student"),
            enrolled_at=datetime.fromisoformat(data["created"]) if data.get("created") else datetime.now(timezone.utc),
            dropped_at=datetime.fromisoformat(data["modified"]) if data.get("modified") and not data.get("active") else None,
            active=data.get("active", True),
        )

    @staticmethod
    def to_assignment(data: Dict[str, Any]) -> Assignment:
        return Assignment(
            id=AssignmentId(value=data["id"]),
            course_id=CourseId(value=data["courseId"]),
            name=data.get("name", ""),
            description=data.get("description"),
            due_date=datetime.fromisoformat(data["dueDate"]) if data.get("dueDate") else None,
            points_possible=float(data.get("points", {}).get("possible", 0.0)),
            created_at=datetime.fromisoformat(data["created"]) if data.get("created") else None,
            updated_at=datetime.fromisoformat(data["modified"]) if data.get("modified") else None,
        )

    @staticmethod
    def to_grade(data: Dict[str, Any]) -> Grade:
        return Grade(
            id=GradeId(value=data.get("id") or f"{data.get('userId')}_{data.get('assignmentId')}"),
            student_id=StudentId(value=data["userId"]),
            assignment_id=AssignmentId(value=data["assignmentId"]),
            score=float(data["score"]) if data.get("score") is not None else None,
            feedback=data.get("feedback"),
            graded_at=datetime.fromisoformat(data["gradedDate"]) if data.get("gradedDate") else None,
            updated_at=datetime.fromisoformat(data["modified"]) if data.get("modified") else None,
        )