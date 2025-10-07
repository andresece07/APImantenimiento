# app/security.py
from passlib.context import CryptContext
from passlib.hash import sha256_crypt # <-- Añade esta importación

pwd_context = CryptContext(schemes=["bcrypt", "sha256_crypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

# --- AÑADE ESTA NUEVA FUNCIÓN ---
def generate_sha256_hash(plain: str) -> str:
    """Genera un hash SHA256 para propósitos de seeding."""
    return sha256_crypt.hash(plain)