# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- 1. IMPORTACIÓN CORREGIDA
from app.config import settings
from app.database import engine, Base

# --- 2. IMPORTACIONES DE ROUTERS CORREGIDAS ---
from app.routers import (
    auth, 
    usuarios, 
    tareas, 
    parametros, 
    actividades,  # <-- Faltaba este
    catalogos     # <-- Faltaba este
)

# No usamos Base.metadata.create_all en producción: usa schema.sql/Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

# --- 3. CONFIGURACIÓN DE CORS ---
# (La que habías añadido, ahora con la importación correcta)
origins = [
    "https://creatic-app.pages.dev",
    "http://127.0.0.1:5500", # Origen de desarrollo frontend
    "http://localhost:5500", # Otro origen común de desarrollo
    "http://184.174.39.191", # IP del servidor (puerto 80)
    "http://184.174.39.191:8000", # IP del servidor (puerto 8000)
    # "http://tu-dominio-web.com", # Cuando despliegues tu web en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- 4. REGISTRO DE TODOS LOS ROUTERS ---
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tareas.router)
app.include_router(parametros.router)
app.include_router(actividades.router)  # <-- Faltaba este
app.include_router(catalogos.router)    # <-- Faltaba este

@app.get("/health")
def health():
    return {"status": "ok"}