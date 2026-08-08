"""Value objects with validation and encapsulation."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class Email(EmailStr):
    pass


class StudentId(BaseModel):
    value: str = Field(..., min_length=1, description="Student UUID or external key")

    def __str__(self) -> str:
        return self.value


class CourseId(BaseModel):
    value: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.value


class EnrollmentId(BaseModel):
    value: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.value


class AssignmentId(BaseModel):
    value: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.value


class GradeId(BaseModel):
    value: str = Field(..., min_length=1)

    def __str__(self) -> str:
        return self.value


class DateRange(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    def is_valid(self) -> bool:
        return self.start is None or self.end is None or self.start <= self.end