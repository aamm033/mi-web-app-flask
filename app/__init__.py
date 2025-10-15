# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config # Importación relativa desde config.py
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# Inicializar extensiones globalmente (pero sin app)
db = SQLAlchemy()
migrate = Migrate() # ⬅️ Instanciar
# 🟢 Instancia Global para Bootstrap (opcional, pero limpio)
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Conectar extensiones a la aplicación
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Lógica requerida por Flask-Login (debe estar cerca de load_user)
    from app.models import Usuario
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # 1. REGISTRAR BLUEPRINTS
    from app.main.routes import main as main_bp
    app.register_blueprint(main_bp)

    from app.auth.routes import auth as auth_bp
    app.register_blueprint(auth_bp)

    return app