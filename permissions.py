from fastapi import HTTPException
from sqlalchemy.orm import Session

import crud
from models import Course, Enrollment, User


def get_course(db: Session, course_id: int):
    course = crud.get_course(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail='Course not found')
    return course


def check_teacher(user: User, course: Course):
    if user.role != 'admin' and not (user.role == 'teacher' and course.teacher_id == user.id):
        raise HTTPException(status_code=403, detail='Only course teacher or admin can manage this course')


def check_enrollment(db: Session, course_id: int, student_id: int):
    enrolled = db.query(Enrollment).filter(Enrollment.course_id == course_id, Enrollment.student_id == student_id).first()
    if not enrolled:
        raise HTTPException(status_code=409, detail='Student is not enrolled in this course')
    return enrolled


def overlap(start_a, end_a, start_b, end_b):
    return start_a < end_b and start_b < end_a
