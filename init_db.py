# init_db.py
import os
from run import app, db # Ajusta las importaciones según tu estructura

# La función create_app() debe estar disponible si es la que usas.
# Si tu objeto Flask se llama 'app' y está en 'run.py', solo ajusta la importación.

with app.app_context():
    # Intenta crear todas las tablas
    db.create_all()
    print("¡Base de datos inicializada exitosamente!")