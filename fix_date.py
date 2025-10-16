# fix_date.py (MODIFICADO para arreglar TODOS los NULLs)
from run import app, db
from app.models import Usuario
from datetime import datetime

with app.app_context():
    # Busca a todos los usuarios donde la fecha es NULL
    usuarios_a_arreglar = Usuario.query.filter(Usuario.fecha_registro.is_(None)).all()

    if usuarios_a_arreglar:
        for user in usuarios_a_arreglar:
            user.fecha_registro = datetime.utcnow()
            print(f"✅ Fecha fijada para: {user.username}")

        db.session.commit()
        print("¡Todos los usuarios sin fecha han sido actualizados!")
    else:
        print("⚠️ No se encontraron usuarios con fecha de registro nula para actualizar.")

# Salir de la consola de Python (si lo ejecutas interactivamente)
# exit()