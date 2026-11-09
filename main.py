from contextlib import asynccontextmanager

from fastapi import FastAPI

import models  # noqa: F401 - register all database tables
from database import Base, engine
from routers import attendance, auth, courses, grades, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title='School Management API',
    description='School backend with staff roles, timetables, enrollment, grades, attendance and reports.',
    version='1.0.0',
    lifespan=lifespan,
)

app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(grades.router)
app.include_router(attendance.router)
app.include_router(reports.router)


@app.get('/', tags=['Health'])
def home():
    return {'message': 'School Management API is running', 'docs': '/docs'}


@app.get('/health', tags=['Health'])
def health_check():
    return {'status': 'ok'}
