# راهنمای سریع فارسی – پروژه مدیریت مدرسه FastAPI

**مناسب برای VS Code و Windows 11.** فایل `README.md` انگلیسی برای GitHub است.

## ۱. نصب و راه‌اندازی

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(48))"
python seed.py --admin-email admin@example.com --admin-password "ChangeThisPassword123!"
uvicorn main:app --reload
```

اگر فقط Python 3.14 نصب داری، `py -3.11` را به `py -3.14` تغییر بده. در صورت خطای اجرای اسکریپت PowerShell از دستور `Set-ExecutionPolicy -Scope Process Bypass` در همان پنجره استفاده کن.

## ۲. ورود و امتحان کردن

آدرس `http://127.0.0.1:8000/docs` را باز کن. با `POST /auth/login` وارد شو؛ ایمیل در فیلد `username` نوشته می‌شود. اکانت‌های آزمایشی:

- مدیر: `admin@example.com`
- معلم: `teacher@example.com`
- دانش‌آموز: `student@example.com`

رمز اولیه هر سه حساب همان رمزی است که هنگام اجرای `seed.py` تعیین می‌کنی.

ترتیب تست: با نقش مدیر یک دانش‌آموز را در کلاس ثبت‌نام کن (`POST /courses/{course_id}/students/{student_id}`)، با نقش معلم آزمون بساز (`POST /courses/{course_id}/assessments`)، نمره وارد کن، جلسه درس اضافه کن و حضورغیاب بزن؛ در پایان با نقش دانش‌آموز خروجی `GET /students/me/report` را مشاهده کن.

## ۳. ساختار برنامه‌نویسی

مانند پروژه‌های قبلی خودت از `main.py`، `database.py`، `models.py`، `schemas.py`، `crud.py` و `routers` استفاده شده. بخش `permissions.py` هم قوانین دسترسی معلم‌ها، دانش‌آموزان و تداخل کلاس‌ها را نگه می‌دارد.

## ۴. اجرای تست‌ها و آپلود

```powershell
python -m pytest -q
```

برای GitHub یک مخزن مستقل `fastapi-school-management` بساز. فایل‌های کد و مستندات پروژه را آپلود کن، ولی `school.db`، `.venv` و `.env` را منتشر نکن.

**توجه:** این پروژه برای نمونه‌کار است. برای اطلاعات واقعی دانش‌آموزان باید حریم خصوصی، کنترل دسترسی و ثبت سوابق تغییرات بیشتر تقویت شود.
