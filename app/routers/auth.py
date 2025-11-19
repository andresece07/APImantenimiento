from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.auth import create_access_token, generate_refresh_token, hash_refresh_token
from app.config import settings
from app.database import SessionLocal
from app.deps import get_db
from app.models import Parametro, RefreshToken, Usuario
from app.schemas import LoginRequest, RefreshRequest, TokenPair
from app.security import verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


def get_param_ttl_minutes(db: Session) -> int:
    try:
        res = db.execute(
            select(Parametro).where(Parametro.clave == "sesion.ttl_minutos")
        ).scalar_one_or_none()
        if res is None:
            return 1440  # fallback seguro (24h)
        try:
            ttl = int(res.valor)
            return max(ttl, 1440)
        except Exception:
            return 1440
    except Exception:
        # Si falla la consulta (ej. tabla no existe), retornamos default
        return 1440


@router.post("/login", response_model=TokenPair)
def login(data: LoginRequest, request: Request, db: Session = Depends(get_db)):
    user = db.execute(
        select(Usuario).where(Usuario.email == data.email)
    ).scalar_one_or_none()
    if (
        not user
        or not verify_password(data.password, user.password_hash)
        or not user.activo
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas"
        )
    # Access corto
    access_token, expires_in = create_access_token(
        user.id, user.rol_id, settings.ACCESS_TOKEN_TTL_MINUTES
    )
    # Refresh gobierna la duración de la sesión en total
    ttl_min = get_param_ttl_minutes(db)
    refresh_raw = generate_refresh_token()
    r = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(refresh_raw),
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=ttl_min),
        revoked=False,
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None,
    )
    # single session per user
    if settings.SINGLE_SESSION_PER_USER:
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id, RefreshToken.revoked == False
        ).update({"revoked": True})
    db.add(r)
    db.commit()
    return TokenPair(
        access_token=access_token, refresh_token=refresh_raw, expires_in=expires_in
    )


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, request: Request, db: Session = Depends(get_db)):
    token_hash = hash_refresh_token(body.refresh_token)
    r = db.query(RefreshToken).filter(RefreshToken.token_hash == token_hash).first()
    if not r or r.revoked:
        raise HTTPException(status_code=401, detail="Refresh inválido")
    if r.expires_at <= datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh expirado")
    # Rotación: revocar el actual y emitir uno nuevo
    r.revoked = True
    db.add(r)
    # Access
    user = db.query(Usuario).filter(Usuario.id == r.user_id).first()
    access_token, expires_in = create_access_token(
        user.id, user.rol_id, settings.ACCESS_TOKEN_TTL_MINUTES
    )
    # Nuevo refresh con el TTL actual de parámetros
    ttl_min = get_param_ttl_minutes(db)
    new_raw = generate_refresh_token()
    new_r = RefreshToken(
        user_id=user.id,
        token_hash=hash_refresh_token(new_raw),
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=ttl_min),
        revoked=False,
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None,
    )
    db.add(new_r)
    db.commit()
    return TokenPair(
        access_token=access_token, refresh_token=new_raw, expires_in=expires_in
    )


@router.post("/logout")
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    token_hash = hash_refresh_token(body.refresh_token)
    r = (
        db.query(RefreshToken)
        .filter(RefreshToken.token_hash == token_hash, RefreshToken.revoked == False)
        .first()
    )
    if not r:
        # idempotente
        return {"ok": True}
    r.revoked = True
    db.add(r)
    db.commit()
    return {"ok": True}
