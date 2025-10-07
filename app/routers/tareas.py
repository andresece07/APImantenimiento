# app/routers/tareas.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from typing import List

from app.deps import get_db, get_current_user
from app.models import Tarea, Usuario, Equipo
from app.schemas import TareaOut, TareaCreate, TareaUpdate

router = APIRouter(prefix="/tareas", tags=["tareas"])

@router.get("", response_model=List[TareaOut])
def list_tareas(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene la lista de tareas.
    - Si el usuario es Supervisor (rol 2), ve todas las tareas.
    - Si es Técnico (rol 1), ve solo las tareas asignadas a él.
    """
    # Carga eficientemente la información del equipo relacionado con cada tarea
    query = select(Tarea).options(selectinload(Tarea.equipo))

    # Filtra las tareas según el rol del usuario
    if user["rol_id"] != 2:
        query = query.where(Tarea.usuario_id == user["id"])

    tareas = db.execute(query).scalars().unique().all()
    return tareas

@router.get("/{tarea_id}", response_model=TareaOut)
def get_tarea(tarea_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene una tarea específica por su ID.
    """
    query = select(Tarea).options(selectinload(Tarea.equipo)).where(Tarea.id == tarea_id)
    tarea = db.execute(query).scalar_one_or_none()

    if not tarea:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    # Un técnico solo puede ver sus propias tareas
    if user["rol_id"] != 2 and tarea.usuario_id != user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permiso para ver esta tarea")

    return tarea

# (Aquí irían los endpoints para crear, actualizar y borrar tareas si los necesitas)