from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Time, UniqueConstraint
from database import Base


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, teacher, student
    created_at = Column(DateTime, default=utc_now)


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    title = Column(String(120), nullable=False)
    teacher_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    capacity = Column(Integer, nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String(40), nullable=False)


class Enrollment(Base):
    __tablename__ = 'enrollments'
    __table_args__ = (UniqueConstraint('course_id', 'student_id', name='uq_course_student'),)

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    joined_at = Column(DateTime, default=utc_now)


class Assessment(Base):
    __tablename__ = 'assessments'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(120), nullable=False)
    max_points = Column(Float, nullable=False)
    weight = Column(Float, nullable=False, default=1.0)


class Grade(Base):
    __tablename__ = 'grades'
    __table_args__ = (UniqueConstraint('assessment_id', 'student_id', name='uq_assessment_student'),)

    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('assessments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    points = Column(Float, nullable=False)


class Lesson(Base):
    __tablename__ = 'lessons'
    __table_args__ = (UniqueConstraint('course_id', 'lesson_date', name='uq_course_lesson'),)

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    lesson_date = Column(Date, nullable=False)
    topic = Column(String(200), nullable=False, default='')


class Attendance(Base):
    __tablename__ = 'attendance'
    __table_args__ = (UniqueConstraint('lesson_id', 'student_id', name='uq_lesson_student'),)

    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late
