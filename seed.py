"""Create example users and one course. Run manually with your own admin password."""
import argparse
from datetime import time

from database import Base, SessionLocal, engine
from models import Course, User
from security import hash_password


def seed(admin_email: str, admin_password: str):
    if len(admin_password) < 8:
        raise ValueError('Admin password must be at least 8 characters')
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        people = [
            ('School Admin', admin_email.lower(), 'admin', admin_password),
            ('Anna Teacher', 'teacher@example.com', 'teacher', admin_password),
            ('Max Student', 'student@example.com', 'student', admin_password),
        ]
        for name, email, role, password in people:
            if not db.query(User).filter(User.email == email).first():
                db.add(User(name=name, email=email, role=role, password=hash_password(password)))
        db.flush()
        teacher = db.query(User).filter(User.email == 'teacher@example.com').first()
        if teacher and not db.query(Course).filter(Course.code == 'PY101').first():
            db.add(Course(code='PY101', title='Introduction to Python', teacher_id=teacher.id,
                          capacity=25, day_of_week=0, start_time=time(9, 0), end_time=time(10, 30), room='B-201'))
        db.commit()
        print('Seed complete. Admin email:', admin_email)
        print('Demo teacher: teacher@example.com | Demo student: student@example.com')
        print('All new accounts use the password passed on the command line.')
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--admin-email', required=True)
    parser.add_argument('--admin-password', required=True)
    args = parser.parse_args()
    seed(args.admin_email, args.admin_password)
