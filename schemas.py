from datetime import date, time
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Literal['teacher', 'student']


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class CourseCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20, pattern=r'^[A-Za-z0-9_-]+$')
    title: str = Field(min_length=3, max_length=120)
    teacher_id: int = Field(gt=0)
    capacity: int = Field(ge=1, le=500)
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    room: str = Field(min_length=1, max_length=40)

    @model_validator(mode='after')
    def check_schedule(self):
        if self.end_time <= self.start_time:
            raise ValueError('End time must be after start time')
        return self


class CourseResponse(CourseCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CourseUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=120)
    capacity: int | None = Field(default=None, ge=1, le=500)
    teacher_id: int | None = Field(default=None, gt=0)
    day_of_week: int | None = Field(default=None, ge=0, le=6)
    start_time: time | None = None
    end_time: time | None = None
    room: str | None = Field(default=None, min_length=1, max_length=40)


class AssessmentCreate(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    max_points: float = Field(gt=0, le=10000, allow_inf_nan=False)
    weight: float = Field(default=1.0, gt=0, le=100, allow_inf_nan=False)


class AssessmentResponse(AssessmentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    course_id: int


class GradeCreate(BaseModel):
    student_id: int = Field(gt=0)
    points: float = Field(ge=0, allow_inf_nan=False)


class LessonCreate(BaseModel):
    lesson_date: date
    topic: str = Field(default='', max_length=200)


class AttendanceCreate(BaseModel):
    student_id: int = Field(gt=0)
    status: Literal['present', 'absent', 'late']
