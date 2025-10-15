# app/config.py

import os


class Config:
    # ⚠️ MUY IMPORTANTE: Cambia esta clave en producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_por_defecto'

    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False