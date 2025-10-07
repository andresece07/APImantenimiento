# app/services/auth_service.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Request

# Se importa Parametro directamente
from app.models import Usuario, RefreshToken, Tarea, Parametro
from app.auth import create_access_token, generate_refresh_token, hash_refresh_token
from app.config import settings
from app.schemas import TokenPair
from sqlalchemy.orm import selectinload # <-- Añade esta importación

# --- ESTA FUNCIÓN SE MUEVE AQUÍ ---
def get_param_ttl_minutes(db: Session) -> int:
    """Obtiene el TTL de la sesión desde la base de datos."""
    res = db.execute(select(Parametro).where(Parametro.clave == "sesion.ttl_minutos")).scalar_one_or_none()
    if res is None:
        return 1440  # fallback seguro (24h)
    try:
        ttl = int(res.valor)
        return max(ttl, 1440)
    except (ValueError, TypeError):
        return 1440

def create_user_session(user: Usuario, db: Session, request: Request) -> TokenPair:
    # ... (el resto de la función se mantiene igual, pero ahora llama a la función local)
    access_token, expires_in = create_access_token(user.id, user.rol_id, settings.ACCESS_TOKEN_TTL_MINUTES)
    refresh_raw = generate_refresh_token()
    token_hash = hash_refresh_token(refresh_raw)
    ttl_minutes = get_param_ttl_minutes(db) # Llama a la función que ahora está en este mismo archivo
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)

    if settings.SINGLE_SESSION_PER_USER:
        db.query(RefreshToken).filter(
            RefreshToken.user_id == user.id, RefreshToken.revoked == False
        ).update({"revoked": True})

    new_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
        user_agent=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None
    )
    db.add(new_refresh_token)
    db.commit()

    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_raw,
        expires_in=expires_in
    )

def get_tasks_for_user(user: Usuario, db: Session) -> list[Tarea]:
    """Obtiene la lista de tareas del usuario, cargando la info del equipo."""
    # Usamos selectinload para cargar eficientemente la info del equipo
    query = select(Tarea).options(selectinload(Tarea.equipo))
    
    # Rol 2 = Supervisor. Si no es supervisor, se filtra por tareas asignadas.
    if user.rol_id != 2:
        query = query.where(Tarea.usuario_id == user.id)
    
    tasks = db.execute(query).scalars().unique().all()
    return tasks