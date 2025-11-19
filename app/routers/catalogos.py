# app/routers/catalogos.py
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.deps import get_db, get_current_user
from app.models import (
    Cliente, Provincia, Equipo, UnidadNegocio, EstadoEquipo,
    Proyecto, Ciudad, Agencia, Usuario
)
from app.schemas import (
    CatalogoCompleto, ClienteOut, ProyectoOut, ProvinciaOut,
    CiudadOut, UnidadNegocioOut, AgenciaOut, UsuarioOut, EstadoEquipoOut
)

router = APIRouter(tags=["catalogos"])

@router.get("/catalogos/all", response_model=CatalogoCompleto)
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

@router.get("/clientes", response_model=List[ClienteOut])
def get_clientes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(Cliente).options(selectinload(Cliente.proyectos))).scalars().unique().all()

@router.get("/proyectos", response_model=List[ProyectoOut])
def get_proyectos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(Proyecto)).scalars().all()

@router.get("/provincias", response_model=List[ProvinciaOut])
def get_provincias(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(Provincia).options(selectinload(Provincia.ciudades))).scalars().unique().all()

@router.get("/ciudades", response_model=List[CiudadOut])
def get_ciudades(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(Ciudad).options(selectinload(Ciudad.agencias))).scalars().unique().all()

@router.get("/unidades_negocio", response_model=List[UnidadNegocioOut])
def get_unidades_negocio(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(UnidadNegocio)).scalars().all()

@router.get("/agencias", response_model=List[AgenciaOut])
def get_agencias(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.execute(select(Agencia)).scalars().all()

@router.get("/tecnicos", response_model=List[UsuarioOut])
def get_tecnicos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Asumiendo rol_id=1 es Técnico (según seeds.sql)
    return db.execute(select(Usuario).where(Usuario.rol_id == 1)).scalars().all()

@router.get("/tipos_equipo", response_model=List[EstadoEquipoOut])
def get_tipos_equipo(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Mapeamos tipos_equipo a EstadoEquipo por ahora para evitar 404
    return db.execute(select(EstadoEquipo)).scalars().all()