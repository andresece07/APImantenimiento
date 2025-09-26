from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.deps import get_db, get_current_user, require_roles
from app.models import Usuario
from app.schemas import UsuarioCreate, UsuarioOut, UsuarioUpdate
from app.security import hash_password

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("", response_model=List[UsuarioOut])
def list_users(db: Session = Depends(get_db), user=Depends(require_roles(2))):  # Supervisor
    rows = db.execute(select(Usuario)).scalars().all()
    return rows

@router.get("/{user_id}", response_model=UsuarioOut)
def get_user(user_id: int, db: Session = Depends(get_db), auth=Depends(get_current_user)):
    u = db.get(Usuario, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if auth["rol_id"] != 2 and auth["id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return u

@router.post("", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_user(body: UsuarioCreate, db: Session = Depends(get_db), user=Depends(require_roles(2))):
    exists = db.execute(select(Usuario).where(Usuario.email == body.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="Email ya registrado")
    u = Usuario(
        nombre=body.nombre,
        email=body.email,
        password_hash=hash_password(body.password),
        rol_id=body.rol_id,
        activo=body.activo
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.patch("/{user_id}", response_model=UsuarioOut)
def update_user(user_id: int, body: UsuarioUpdate, db: Session = Depends(get_db), auth=Depends(get_current_user)):
    u = db.get(Usuario, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if auth["rol_id"] != 2 and auth["id"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if body.nombre is not None: u.nombre = body.nombre
    if body.password is not None: u.password_hash = hash_password(body.password)
    if body.rol_id is not None:
        if auth["rol_id"] != 2:
            raise HTTPException(status_code=403, detail="Sólo supervisor puede cambiar rol")
        u.rol_id = body.rol_id
    if body.activo is not None:
        if auth["rol_id"] != 2:
            raise HTTPException(status_code=403, detail="Sólo supervisor puede (des)activar")
        u.activo = body.activo

    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user=Depends(require_roles(2))):
    u = db.get(Usuario, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(u)
    db.commit()
    return {"ok": True}
