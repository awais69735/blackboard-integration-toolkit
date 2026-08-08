"""Core domain entities with business logic and validation."""

from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime, timezone
from .value_objects import (
    Email, StudentId, CourseId, EnrollmentId, AssignmentId, GradeId, DateRange
)


class Student(BaseModel):
    """A student (user) in the learning system."""
    id: StudentId
    username: str = Field(..., min_length=1, max_length=50)
    email: Email
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @model_validator(mode="before")
    @classmethod
    def validate_username(cls, values):
        # Example: ensure username is lowercased
        if "username" in values:
            values["username"] = values["username"].lower().strip()
        return values


class Course(BaseModel):
    """A course offering."""
    id: CourseId
    name: str = Field(..., min_length=1, max_length=255)
    code: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    term: Optional[str] = None
    date_range: DateRange = DateRange()
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Enrollment(BaseModel):
    """Enrollment of a student in a course."""
    id: EnrollmentId
    student_id: StudentId
    course_id: CourseId
    role: str = Field(..., pattern="^(student|instructor|ta|auditor)$")
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    dropped_at: Optional[datetime] = None
    active: bool = True

    def drop(self) -> None:
        """Drop the enrollment."""
        self.active = False
        self.dropped_at = datetime.now(timezone.utc)


class Assignment(BaseModel):
    id: Optional[AssignmentId] = None
    course_id: CourseId
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    points_possible: float = Field(ge=0.0)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Grade(BaseModel):
    """A grade entry for a student on an assignment."""
    id: GradeId
    student_id: StudentId
    assignment_id: AssignmentId
    score: Optional[float] = Field(None, ge=0.0)
    feedback: Optional[str] = None
    graded_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def is_graded(self) -> bool:
        return self.score is not None

    def grade(self, score: float, feedback: Optional[str] = None) -> None:
        """Apply a grade (with validation)."""
        if score < 0:
            raise ValueError("Score cannot be negative")
        self.score = score
        self.feedback = feedback
        self.graded_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)