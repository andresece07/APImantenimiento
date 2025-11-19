# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, parametros, tareas, usuarios, catalogos

# No usamos Base.metadata.create_all en producción: usa schema.sql/Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# 1. Define los orígenes (dominios) que tienen permiso
origins = [
    "https://creatic-app.pages.dev",  # Tu frontend en producción
    "http://127.0.0.1:5500",  # Tu frontend de desarrollo local
    "http://localhost:5500",  # Alternativa local
]

# 2. Agrega el middleware de CORS a tu aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite los orígenes de la lista
    allow_credentials=True,  # Permite cookies (importante para auth)
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Permite todas las cabeceras
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tareas.router)
app.include_router(parametros.router)
app.include_router(catalogos.router)


@app.get("/health")
def health():
    return {"status": "ok"}
