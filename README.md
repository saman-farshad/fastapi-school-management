# School Management API 🎓

A FastAPI REST backend for a school or educational center. Built as a portfolio project with schedule conflict detection, enrollment rules, assessment weighting and individual student reports.

**Developer:** Saman Farshad  
**Stack:** Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic 2, SQLite, JWT, pytest  
**Interactive API documentation:** `/docs`

## Features

- JWT login and three access roles: **admin**, **teacher** and **student**
- Admin-created teacher/student accounts (no public sign-ups)
- Course CRUD with teacher, room, capacity, weekday and time
- Automatic **teacher schedule and classroom collision detection**
- Enrollment with capacity, duplication and **student timetable** conflict checks
- Teachers can create graded assessments with configurable `max_points` and `weight`
- Grades are editable and never allowed to exceed the assessment maximum
- Gradebook with **weighted percentage** for graded assessments (ungraded work is omitted)
- Scheduled lessons and attendance records: `present`, `absent`, `late`
- Lesson dates must match the course's weekday
- Teacher/admin attendance report; late counts as present
- Students can view **only their own** grades and attendance at `/students/me/report`
- Admin dashboard, demo seed, isolated API tests and GitHub Actions

## Project structure

```text
fastapi-school-management/
├── main.py                 # FastAPI app and routers
├── database.py             # SQLAlchemy engine + session
├── models.py               # Users, courses, enrollments, assessments, grades, lessons...
├── schemas.py              # Request validation
├── crud.py                 # create_user, get_users, create_course, ...
├── security.py             # Password hashing, JWT, role checks
├── permissions.py          # Enrollment / teacher / timetable checks
├── seed.py                 # Development demo data
├── routers/
│   ├── auth.py             # Staff login and admin user creation
│   ├── courses.py          # Courses and enrollment
│   ├── grades.py           # Assessments and grades
│   ├── attendance.py       # Lessons and attendance
│   └── reports.py          # Student and admin reports
├── tests/
├── examples.http
├── Dockerfile
└── .github/workflows/tests.yml
```

## Run on Windows 11 / VS Code (PowerShell)

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
python seed.py --admin-email admin@example.com --admin-password "ChangeThisPassword123!"
uvicorn main:app --reload
```

If you only have a supported newer Python version (such as 3.14), replace `py -3.11` accordingly.

Go to **http://127.0.0.1:8000/docs**. The SQLite `school.db` is created automatically and excluded from Git.

### Demo accounts

`seed.py` creates these **local development accounts** if they do not already exist:

| Role | Login email | Password |
|---|---|---|
| Admin | The address passed to `--admin-email` | The password passed to `--admin-password` |
| Teacher | `teacher@example.com` | The same password |
| Student | `student@example.com` | The same password |

Never reuse these sample credentials or the development secret in a real deployment. The seed script doesn't reset existing user passwords.

### Login and authorization in Swagger

Use **POST `/auth/login`** with `username` set to an email and the selected password. In Swagger, click **Authorize** and enter the credentials in the OAuth login form. Different endpoints are visible to different roles.

## Practical demo from start to finish

1. Use the admin account to create a teacher/student with `POST /users`, or use the seeded accounts.
2. Use the seed-created course `PY101`, or create another course with `POST /courses`.
3. Enroll the student using `POST /courses/{course_id}/students/{student_id}` (admin).
4. Log in as the teacher, create an assessment using `POST /courses/{course_id}/assessments`.
5. Record a grade using `PUT /assessments/{assessment_id}/grades`.
6. Create a lesson on the course's weekday using `POST /courses/{course_id}/lessons`.
7. Record attendance using `PUT /lessons/{lesson_id}/attendance`.
8. Log in as the student and open `GET /students/me/report`.

Example course:

```json
{
  "code": "DS101",
  "title": "Python and Data Science",
  "teacher_id": 2,
  "capacity": 20,
  "day_of_week": 0,
  "start_time": "09:00:00",
  "end_time": "10:30:00",
  "room": "A-101"
}
```

`day_of_week` follows Python's convention: 0 = Monday, 6 = Sunday. All timetable intervals are half-open: 09:00–10:00 does not conflict with 10:00–11:00.

### How weighted grades work

Each assessment has a maximum and a weight. Suppose a student has:

- Quiz: `8 / 10`, weight `1`
- Final: `36 / 40`, weight `2`

The reported grade is: `(0.80 × 1 + 0.90 × 2) / (1 + 2) × 100 = 86.67%`.
Missing grades are excluded from this average instead of being treated as zero.

### How attendance works

A student with 2 `present`, 1 `late`, and 1 `absent` has `75%` attendance. Sessions not yet marked for that student are not included in the denominator.

## Selected endpoints

| Method | Endpoint | Access |
|---|---|---|
| POST | `/auth/login` | Public |
| POST / GET | `/users` | Admin |
| POST / PATCH | `/courses` / `/courses/{id}` | Admin |
| POST | `/courses/{id}/students/{student_id}` | Admin |
| GET | `/courses/{id}/students` | Admin / course teacher |
| POST | `/courses/{id}/assessments` | Admin / course teacher |
| PUT | `/assessments/{id}/grades` | Admin / course teacher |
| GET | `/courses/{id}/gradebook` | Admin / course teacher |
| POST | `/courses/{id}/lessons` | Admin / course teacher |
| PUT | `/lessons/{id}/attendance` | Admin / course teacher |
| GET | `/students/me/report` | Student |
| GET | `/admin/dashboard` | Admin |

## Run tests

```powershell
python -m pytest -q
```

Tests cover login, role permissions, overlapping schedules, course capacity, duplicate enrollments, student timetable conflicts, grade validation, attendance and private student reports.

## Run with Docker (optional)

```powershell
docker build -t saman-school-api .
docker run --rm -p 8000:8000 -e SECRET_KEY="your-own-secret-of-at-least-32-characters" saman-school-api
```

## Notes on scope

This is an educational **backend prototype**, not a production school information system. It does not implement report-card PDFs, parent portals, audit trails, GDPR retention policies, Alembic migrations or concurrency-safe enrollment limits under heavy load. Do not upload real student personal data to a demo. For production, use PostgreSQL, improve database-level timetable/enrollment coordination, configure a strong private `SECRET_KEY`, and add HTTPS, rate limiting and audit logs.

---

**Portfolio focus:** straightforward Python naming, SQLAlchemy models, REST endpoints and practical school business logic.
