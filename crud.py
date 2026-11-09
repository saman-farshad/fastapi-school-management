"""Classic CRUD helpers, using the same SQLAlchemy db.query() style."""
from sqlalchemy.orm import Session

import models
from security import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, role=None, skip=0, limit=50):
    query = db.query(models.User)
    if role:
        query = query.filter(models.User.role == role)
    return query.order_by(models.User.id).offset(skip).limit(limit).all()


def create_user(db: Session, user_data):
    new_user = models.User(
        name=user_data.name,
        email=str(user_data.email).lower(),
        password=hash_password(user_data.password),
        role=user_data.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_courses(db: Session, day_of_week=None, skip=0, limit=50):
    query = db.query(models.Course)
    if day_of_week is not None:
        query = query.filter(models.Course.day_of_week == day_of_week)
    return query.order_by(models.Course.id).offset(skip).limit(limit).all()


def create_course(db: Session, course_data):
    new_course = models.Course(**{**course_data.model_dump(), 'code': course_data.code.upper()})
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course


def update_course(db: Session, course, course_data):
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


def create_enrollment(db: Session, course_id: int, student_id: int):
    enrollment = models.Enrollment(course_id=course_id, student_id=student_id)
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


def delete_enrollment(db: Session, enrollment):
    db.delete(enrollment)
    db.commit()
