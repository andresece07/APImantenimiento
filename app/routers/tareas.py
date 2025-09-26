from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from app.deps import get_db, get_current_user, require_roles
from app.models import Tarea, Usuario
from app.schemas import TareaCreate, TareaUpdate, TareaOut

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get("", response_model=List[TareaOut])
def list_tareas(db: Session = Depends(get_db), auth=Depends(get_current_user)):
    q = select(Tarea)
    if auth["rol_id"] != 2:  # Tecnico solo ve las suyas
        q = q.where((Tarea.usuario_id == auth["id"]) | (Tarea.creada_por == auth["id"]))
    return db.execute(q).scalars().all()

@router.get("/{tarea_id}", response_model=TareaOut)
def get_tarea(tarea_id: int, db: Session = Depends(get_db), auth=Depends(get_current_user)):
    t = db.get(Tarea, tarea_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if auth["rol_id"] != 2 and auth["id"] not in [t.usuario_id, t.creada_por]:
        raise HTTPException(status_code=403, detail="Forbidden")
    return t

@router.post("", response_model=TareaOut)
def create_tarea(body: TareaCreate, db: Session = Depends(get_db), user=Depends(require_roles(2))):
    t = Tarea(
        titulo=body.titulo,
        descripcion=body.descripcion,
        estado=body.estado or "pendiente",
        usuario_id=body.usuario_id,
        creada_por=user["id"]
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.patch("/{tarea_id}", response_model=TareaOut)
def update_tarea(tarea_id: int, body: TareaUpdate, db: Session = Depends(get_db), auth=Depends(get_current_user)):
    t = db.get(Tarea, tarea_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    if auth["rol_id"] != 2 and auth["id"] not in [t.usuario_id, t.creada_por]:
        raise HTTPException(status_code=403, detail="Forbidden")

    if body.titulo is not None: t.titulo = body.titulo
    if body.descripcion is not None: t.descripcion = body.descripcion
    if body.estado is not None:
        if auth["rol_id"] != 2 and body.estado not in ["en_progreso","completada","cancelada","pendiente"]:
            pass  # ya validado por Pydantic
        t.estado = body.estado
    if body.usuario_id is not None:
        if auth["rol_id"] != 2:
            raise HTTPException(status_code=403, detail="Sólo supervisor reasigna")
        t.usuario_id = body.usuario_id

    db.add(t)
    db.commit()
    db.refresh(t)
    return t

@router.delete("/{tarea_id}")
def delete_tarea(tarea_id: int, db: Session = Depends(get_db), user=Depends(require_roles(2))):
    t = db.get(Tarea, tarea_id)
    if not t:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    db.delete(t)
    db.commit()
    return {"ok": True}
