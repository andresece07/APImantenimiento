# app/models.py
from datetime import datetime
import enum
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, Enum as SQLAlchemyEnum, Text, CHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

# --- Modelos de Autenticación y Sistema ---

class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(160), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    rol_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(CHAR(64), unique=True, nullable=False)
    issued_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip: Mapped[str | None] = mapped_column(String(64), nullable=True)

class Parametro(Base):
    __tablename__ = "parametros"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    clave: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    valor: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[str] = mapped_column(SQLAlchemyEnum("int","string","bool","json", name="param_tipo"), default="string", nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(255), nullable=True)

# --- Modelos de Catálogos del Negocio ---

class Cliente(Base):
    __tablename__ = "clientes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    nombre_completo: Mapped[str | None] = mapped_column(String(255))
    proyectos: Mapped[list["Proyecto"]] = relationship("Proyecto", back_populates="cliente")

class Proyecto(Base):
    __tablename__ = "proyectos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(Text, nullable=False)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"), nullable=False)
    cliente: Mapped["Cliente"] = relationship("Cliente", back_populates="proyectos")

class Provincia(Base):
    __tablename__ = "provincias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    ciudades: Mapped[list["Ciudad"]] = relationship("Ciudad")

class Ciudad(Base):
    __tablename__ = "ciudades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincias.id"), nullable=False)
    agencias: Mapped[list["Agencia"]] = relationship("Agencia")

class UnidadNegocio(Base):
    __tablename__ = "unidades_negocio"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)

class Agencia(Base):
    __tablename__ = "agencias"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudades.id"), nullable=False)
    unidad_negocio_id: Mapped[int] = mapped_column(ForeignKey("unidades_negocio.id"), nullable=False)

class EstadoEquipo(Base):
    __tablename__ = "estados_equipo"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

class Equipo(Base):
    __tablename__ = "equipos"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    caracteristicas: Mapped[str | None] = mapped_column(Text)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    proyecto_id: Mapped[int] = mapped_column(ForeignKey("proyectos.id"))
    provincia_id: Mapped[int] = mapped_column(ForeignKey("provincias.id"))
    ciudad_id: Mapped[int] = mapped_column(ForeignKey("ciudades.id"))
    unidad_negocio_id: Mapped[int] = mapped_column(ForeignKey("unidades_negocio.id"))
    agencia_id: Mapped[int] = mapped_column(ForeignKey("agencias.id"))
    estado_id: Mapped[int] = mapped_column(ForeignKey("estados_equipo.id"))

# --- Modelos Operativos ---

class Tarea(Base):
    __tablename__ = "tareas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False, index=True)
    equipo_id: Mapped[str] = mapped_column(ForeignKey("equipos.id"), nullable=False, index=True)
    equipo: Mapped["Equipo"] = relationship()