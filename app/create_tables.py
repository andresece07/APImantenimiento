# create_tables.py
from app.database import engine, Base

# Importa todos tus modelos para que SQLAlchemy los conozca
from app.models import (
    Role, Usuario, Parametro, RefreshToken, Tarea,
    Cliente, Proyecto, Provincia, Ciudad, UnidadNegocio, Agencia, Equipo
)

print("Conectando a la base de datos para crear las tablas...")

# Esta línea es la magia: lee todos los modelos (planos) y los crea en la base de datos
Base.metadata.create_all(bind=engine)

print("¡Tablas creadas exitosamente (si no existían ya)!")