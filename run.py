# run.py

from app import create_app, db
from app.models import Usuario, Mensaje

app = create_app()

if __name__ == '__main__':
    # Este bloque solo se usa para ejecutar el servidor.
    # No es la forma estándar de crear tablas, pero funciona para el desarrollo.
    with app.app_context():
        db.create_all()
    app.run(debug=True)