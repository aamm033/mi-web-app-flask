# Script para ejecutar en la consola de Render (o en un archivo temporal)

from run import app, db
from app.models import Usuario

with app.app_context():
    # Consulta para obtener los objetos Usuario donde fecha_registro es NULL
    usuarios_sin_fecha = db.session.query(Usuario).filter(Usuario.fecha_registro.is_(None)).all()

    print("-" * 50)
    print("USUARIOS SIN FECHA REGISTRADA:")

    if usuarios_sin_fecha:
        for user in usuarios_sin_fecha:
            # Imprime el ID y el username para identificación
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    else:
        print("✅ ¡No hay usuarios con fecha de registro nula!")

    print("-" * 50)

# Salir de la consola de Python (si lo ejecutas interactivamente)
# exit()