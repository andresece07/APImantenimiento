# hash_util.py
# ¡Importamos la nueva función!
from app.security import generate_sha256_hash

password_to_hash = "123"

# ¡Y la usamos aquí!
hashed_password = generate_sha256_hash(password_to_hash)

print("--- COPIA Y PEGA ESTE HASH (SHA256) EN TU BD ---")
print(hashed_password)
print("-------------------------------------------------")