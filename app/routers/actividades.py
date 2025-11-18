# app/routers/actividades.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from typing import List
from app.deps import get_db, get_current_user
from app.models import Actividad 
from app.schemas import ActividadOut 

router = APIRouter(prefix="/actividades", tags=["actividades"])

@router.get("", response_model=List[ActividadOut])
def list_activities(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """
    Obtiene el catálogo completo de actividades de mantenimiento.
    """
    # Carga las respuestas relacionadas de forma eficiente
    query = select(Actividad).options(selectinload(Actividad.posibles_respuestas))
    result = db.execute(query).scalars().unique().all()
    return result