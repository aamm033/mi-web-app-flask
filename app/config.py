# app/config.py

import os


# ...

class Config:
    # ⚠️ MUY IMPORTANTE: Cambia esta clave en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_por_defecto'

    # 🟢 CAMBIO CRÍTICO PARA PRODUCCIÓN:
    # Usará la variable de entorno DATABASE_URL en Render.
    # Si no existe (localmente), usará SQLite para desarrollo.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False