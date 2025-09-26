from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.deps import get_db, require_roles
from app.models import Parametro
from app.schemas import SesionTTL

router = APIRouter(prefix="/parametros", tags=["parametros"])

@router.get("/sesion-ttl", response_model=SesionTTL)
def get_sesion_ttl(db: Session = Depends(get_db), user=Depends(require_roles(2))):  # Supervisor=2
    p = db.execute(select(Parametro).where(Parametro.clave == "sesion.ttl_minutos")).scalar_one_or_none()
    if not p:
        return {"ttl_minutos": 1440}
    return {"ttl_minutos": max(int(p.valor), 1440)}

@router.patch("/sesion-ttl", response_model=SesionTTL)
def set_sesion_ttl(body: SesionTTL, db: Session = Depends(get_db), user=Depends(require_roles(2))):
    if body.ttl_minutos < 1440:
        raise HTTPException(status_code=400, detail="El TTL mínimo es 1440 minutos (24h)")
    p = db.execute(select(Parametro).where(Parametro.clave == "sesion.ttl_minutos")).scalar_one_or_none()
    if not p:
        p = Parametro(clave="sesion.ttl_minutos", valor=str(body.ttl_minutos), tipo="int", descripcion="Duración de la sesión en minutos (min 24h)")
        db.add(p)
    else:
        p.valor = str(body.ttl_minutos)
    db.commit()
    return {"ttl_minutos": int(p.valor)}
