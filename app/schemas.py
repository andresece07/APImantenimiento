# app/schemas.py
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

# --- Schemas de Autenticación y Sistema ---
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class SesionTTL(BaseModel):
    ttl_minutos: int

# --- Schemas de Entidades Base ---
class UsuarioOut(BaseModel):
    id: int
    nombre: str
    email: str
    rol_id: int
    activo: bool
    class Config: from_attributes = True

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(min_length=8)
    rol_id: int
    activo: bool = True

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)
    rol_id: Optional[int] = None
    activo: Optional[bool] = None

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

# --- Schemas de Catálogos ---
class ProyectoOut(BaseModel):
    id: int
    nombre: str
    class Config: from_attributes = True

class ClienteOut(BaseModel):
    id: int
    nombre: str
    nombre_completo: Optional[str] = None
    proyectos: List[ProyectoOut] = []
    class Config: from_attributes = True

class AgenciaOut(BaseModel):
    id: int
    nombre: str
    unidad_negocio_id: int
    class Config: from_attributes = True

class CiudadOut(BaseModel):
    id: int
    nombre: str
    agencias: List[AgenciaOut] = []
    class Config: from_attributes = True

class ProvinciaOut(BaseModel):
    id: int
    nombre: str
    ciudades: List[CiudadOut] = []
    class Config: from_attributes = True

class UnidadNegocioOut(BaseModel):
    id: int
    nombre: str
    class Config: from_attributes = True

class EstadoEquipoOut(BaseModel):
    id: int
    nombre: str
    class Config: from_attributes = True

class EquipoOut(BaseModel):
    id: str
    nombre: str
    modelo: str
    caracteristicas: Optional[str] = None
    cliente_id: int
    proyecto_id: int
    provincia_id: int
    ciudad_id: int
    unidad_negocio_id: int
    agencia_id: int
    estado_id: int
    class Config: from_attributes = True

class TareaOut(BaseModel):
    id: int
    usuario_id: int
    equipo: EquipoOut
    class Config: from_attributes = True

class TareaCreate(BaseModel):
    usuario_id: int
    equipo_id: str

class TareaUpdate(BaseModel):
    usuario_id: Optional[int] = None
    equipo_id: Optional[str] = None

# --- Schemas de Respuestas Compuestas de API ---
class LoginResponse(BaseModel):
    tokens: TokenPair
    user: UsuarioOut
    tasks: List[TareaOut] = []

class CatalogoCompleto(BaseModel):
    clientes: List[ClienteOut]
    ubicaciones: List[ProvinciaOut]
    equipos: List[EquipoOut]
    unidades_negocio: List[UnidadNegocioOut]
    estados_equipo: List[EstadoEquipoOut]