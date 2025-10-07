# app/deps.py
from fastapi import Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session
from jwt import PyJWTError
from typing import Optional

from app.database import SessionLocal
from app.auth import decode_token
from app.config import settings

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
    except PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid or expired token: {e}")

    return {"id": int(payload.get("sub")), "rol_id": int(payload.get("rolId"))}

# --- AÑADE ESTA FUNCIÓN DE VUELTA ---
def require_roles(*roles):
    """
    Dependencia que verifica si el usuario actual tiene uno de los roles requeridos.
    """
    def wrapper(user: dict = Depends(get_current_user)):
        if user["rol_id"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a este recurso."
            )
        return user
    return wrapper