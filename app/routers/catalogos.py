# app/routers/catalogos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.deps import get_db, get_current_user
from app.models import Cliente, Provincia, Equipo, UnidadNegocio, EstadoEquipo
from app.schemas import CatalogoCompleto # Asegúrate de que este schema exista

router = APIRouter(prefix="/catalogos", tags=["catalogos"])

@router.get("/all", response_model=CatalogoCompleto)
def get_all_catalogs(db: Session = Depends(get_db), user=Depends(get_current_user)):
    clientes = db.execute(select(Cliente).options(selectinload(Cliente.proyectos))).scalars().unique().all()
    equipos = db.execute(select(Equipo)).scalars().all()
    unidades_negocio = db.execute(select(UnidadNegocio)).scalars().all()
    estados_equipo = db.execute(select(EstadoEquipo)).scalars().all()
    ubicaciones = db.execute(
        select(Provincia).options(selectinload(Provincia.ciudades).selectinload(Ciudad.agencias))
    ).scalars().unique().all()
    
    return {
        "clientes": clientes,
        "ubicaciones": ubicaciones,
        "equipos": equipos,
        "unidades_negocio": unidades_negocio,
        "estados_equipo": estados_equipo
    }