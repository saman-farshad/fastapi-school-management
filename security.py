import hashlib
import hmac
import os
import secrets
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from database import get_db
from models import User

SECRET_KEY = os.getenv('SECRET_KEY', 'development-only-change-me-please-set-secret-key')
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def hash_password(password: str):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 500_000)
    return f'{salt.hex()}:{digest.hex()}'


def verify_password(password: str, saved_password: str):
    try:
        salt_hex, digest_hex = saved_password.split(':', 1)
        check = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt_hex), 500_000)
        return hmac.compare_digest(check, bytes.fromhex(digest_hex))
    except (ValueError, TypeError):
        return False


def create_access_token(user_id: int):
    now = datetime.now(timezone.utc)
    payload = {'sub': str(user_id), 'iat': now, 'exp': now + timedelta(hours=8)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token', headers={'WWW-Authenticate': 'Bearer'})
    try:
        user_id = int(jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])['sub'])
    except (InvalidTokenError, KeyError, ValueError, TypeError):
        raise error
    user = db.get(User, user_id)
    if not user:
        raise error
    return user


def get_admin(user: User = Depends(get_current_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')
    return user
