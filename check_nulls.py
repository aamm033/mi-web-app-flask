# Script para ejecutar en la consola de Render

from run import app, db
from app.models import Usuario
from sqlalchemy import func  # Necesario para algunas versiones de SQLAlchemy

with app.app_context():
    # Consulta para contar usuarios donde fecha_registro es NULL
    # 'is_(None)' es el equivalente de SQLAlchemy a 'IS NULL' en SQL
    count = db.session.query(Usuario).filter(Usuario.fecha_registro.is_(None)).count()

    print("-" * 50)
    print(f"✅ USUARIOS SIN FECHA REGISTRADA (NULL): {count}")
    print("-" * 50)

# Salir de la consola de Python (si lo ejecutas interactivamente)
# exit()