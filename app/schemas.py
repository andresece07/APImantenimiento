from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# ---- Auth ----
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds for access

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class RefreshRequest(BaseModel):
    refresh_token: str

# ---- Usuario ----
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol_id: int
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8)

class UsuarioOut(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)
    rol_id: Optional[int] = None
    activo: Optional[bool] = None

# ---- Tarea ----
class TareaBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: Optional[Literal['pendiente','en_progreso','completada','cancelada']] = "pendiente"
    usuario_id: Optional[int] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[Literal['pendiente','en_progreso','completada','cancelada']] = None
    usuario_id: Optional[int] = None

class TareaOut(TareaBase):
    id: int
    creada_por: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

# ---- Parametros ----
class SesionTTL(BaseModel):
    ttl_minutos: int
