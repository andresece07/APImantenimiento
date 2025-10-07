# app/auth.py
import jwt
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Optional, Tuple
from app.config import settings

def now_utc() -> datetime:
    return datetime.now(tz=timezone.utc)

def create_access_token(sub: int, rol_id: int, minutes: int) -> Tuple[str, int]:
    exp = now_utc() + timedelta(minutes=minutes)
    # Aseguramos que el 'sub' sea un string para cumplir con el estándar JWT
    payload = {"sub": str(sub), "rolId": rol_id, "exp": int(exp.timestamp())}
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return token, int(minutes * 60)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])

def hash_refresh_token(raw: str) -> str:
    return sha256(raw.encode("utf-8")).hexdigest()

def generate_refresh_token() -> str:
    import secrets
    return secrets.token_urlsafe(48)