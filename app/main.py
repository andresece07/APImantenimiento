#main.py
from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.routers import auth, usuarios, tareas, parametros

# No usamos Base.metadata.create_all en producción: usa schema.sql/Alembic
# Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(tareas.router)
app.include_router(parametros.router)

@app.get("/health")
def health():
    return {"status": "ok"}
