from fastapi import Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.auth import decode_token
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    token = authorization.split()[1]
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return {"id": int(payload.get("sub")), "rol_id": int(payload.get("rolId"))}

def require_roles(*roles):
    def wrapper(user = Depends(get_current_user)):
        if user["rol_id"] not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper
