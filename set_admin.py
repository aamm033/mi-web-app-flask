# set_admin.py
import os
from run import app, db
from app.models import Usuario

# ⚠️ CAMBIA ESTE VALOR con el nombre de usuario correcto
NOMBRE_USUARIO_ADMIN = 'admin'

with app.app_context():
    admin_user = Usuario.query.filter_by(username=NOMBRE_USUARIO_ADMIN).first()

    if admin_user:
        admin_user.is_admin = True
        db.session.commit()
        print(f"✅ ¡Éxito! El usuario '{NOMBRE_USUARIO_ADMIN}' es ahora administrador.")
    else:
        print(f"❌ Error: No se encontró el usuario '{NOMBRE_USUARIO_ADMIN}'.")