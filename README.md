# Backend Mantenimiento (FastAPI)

Autenticación con JWT (access + refresh), RBAC por roles y sesión cuyo **TTL se lee desde la tabla `parametros`** (`sesion.ttl_minutos`, mínimo 1440 = 24h con trigger).

## Requisitos
- Python 3.10+
- MariaDB 10.5+ (o MySQL compatible)
- (Opcional) Apache/Nginx como proxy reverso

## Pasos rápidos
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# crea BD y tablas
mysql -u root -p < schema.sql

# crear usuario de app y datos de ejemplo
mysql -u root -p mantenimiento < seeds.sql

# ejecutar dev
uvicorn app.main:app --reload --port 8000
```

## Endpoints clave
- `POST /auth/login` (usuario/contraseña) → Access + Refresh
- `POST /auth/refresh` → nuevo Access (si el refresh sigue vigente)
- `POST /auth/logout` → revoca refresh actual
- `GET /parametros/sesion-ttl` (Supervisor)
- `PATCH /parametros/sesion-ttl` (Supervisor)
- CRUD de usuarios y tareas con RBAC

## Despliegue (Apache → Uvicorn)
Ejemplo en `deployment/apache.conf`. Habilita proxy y SSL, ejecuta el servicio uvicorn con systemd.

## Seguridad
- Passwords con `bcrypt` (Passlib)
- Refresh tokens **hasheados** en DB y **rotación** en cada refresh
- TTL de sesión **única fuente**: `parametros.sesion.ttl_minutos` (mín. 24h)
- Opción `SINGLE_SESSION_PER_USER` para permitir una sola sesión vigente por usuario
