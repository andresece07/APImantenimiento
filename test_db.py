# test_db.py
import sqlalchemy
from sqlalchemy import text
from app.database import engine # Reutilizamos el motor de tu app

print("Intentando conectar a la base de datos...")

try:
    # Intentar establecer una conexión
    with engine.connect() as connection:
        print("¡Conexión exitosa!")
        
        # Opcional: Ejecutar una consulta simple para verificar
        result = connection.execute(text("SELECT 1"))
        for row in result:
            print("Resultado de la consulta de prueba (SELECT 1):", row[0])
            
    print("La prueba de conexión finalizó correctamente.")

except sqlalchemy.exc.OperationalError as e:
    print("\nError: No se pudo conectar a la base de datos.")
    print("-------------------------------------------------")
    print("Posibles causas:")
    print("1. El servidor de base de datos no está en ejecución.")
    print("2. Las credenciales (usuario, contraseña, host, puerto) en tu archivo .env son incorrectas.")
    print("3. Un firewall está bloqueando la conexión.")
    print("4. El nombre de la base de datos no existe.")
    print("\nDetalles del error original:")
    print(e)

except Exception as e:
    print(f"\nOcurrió un error inesperado: {e}")