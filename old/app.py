# app.py

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # Necesario para el campo fecha (importar al inicio)
from forms import ContactoForm, RegistroForm, LoginForm
from flask_login import login_manager, UserMixin, login_user, logout_user, login_required, current_user

# Inicializa la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dAOWNwDL9gqgys9z' # ¡Cámbiala por una cadena larga y aleatoria!
# ...
# 1. Configurar la base de datos (SQLite, guardada en un archivo llamado 'site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Recomendado para silenciar advertencias
db = SQLAlchemy(app) # Inicializa la extensión
#modelo de base de datos
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Mensaje('{self.nombre}', '{self.fecha}')"

# Define la ruta principal (cuando el usuario visita '/')
@app.route('/')
def inicio():
    # Renderiza el archivo HTML dentro de la carpeta 'templates'
    return render_template('index.html', titulo='Mi primera Web con Python')

# Puedes definir otra ruta, por ejemplo, para una página "Acerca de"
@app.route('/acerca')
def acerca():
    return '¡Hola desde la página Acerca de!'

@app.route('/usuario/<nombre>')
def perfil_usuario(nombre):
    # 'nombre' se convierte en una variable de Python
    return f'Hola, {nombre.capitalize()}. ¡Este es tu perfil!'


from flask import request, Flask


# Permite las peticiones GET (para ver el formulario) y POST (para enviar los datos)
# app.py (Ruta /contacto)

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()  # Instancia el formulario importado

    # form.validate_on_submit() verifica POST y la validez de los datos
    if form.validate_on_submit():
        # Accede a los datos con form.<campo>.data
        nuevo_mensaje = Mensaje(nombre=form.nombre.data, mensaje=form.mensaje.data)
        db.session.add(nuevo_mensaje)
        db.session.commit()

        # Mensaje de éxito
        flash('¡Gracias! Tu mensaje ha sido enviado con éxito.', 'success')
        return redirect(url_for('contacto'))

        # GET: Pasa el objeto 'form' al template
    return render_template('contacto.html', form=form)


@app.route('/mensajes')
@login_required  # ⬅️ ESTO HACE LA MAGIA
def ver_mensajes():
    # 1. Obtener TODOS los mensajes de la base de datos (Consulta: READ)
    # El método .all() trae todos los registros de la tabla Mensaje.
    todos_los_mensajes = Mensaje.query.all()

    # 2. Renderizar una nueva plantilla, pasándole los datos
    return render_template('mensajes.html', mensajes=todos_los_mensajes)

@app.route('/mensaje/eliminar/<int:mensaje_id>', methods=['POST'])
def eliminar_mensaje(mensaje_id):
    # 1. Buscar el mensaje por ID o devolver 404 si no existe
    mensaje_a_eliminar = Mensaje.query.get_or_404(mensaje_id)

    # 2. Borrar y guardar (commit)
    db.session.delete(mensaje_a_eliminar)
    db.session.commit()

    # 3. Redirigir de vuelta a la lista de mensajes
    return redirect(url_for('ver_mensajes'))

@app.route('/mensaje/editar/<int:mensaje_id>', methods=['GET', 'POST'])
def editar_mensaje(mensaje_id):
    mensaje_a_editar = Mensaje.query.get_or_404(mensaje_id)

    if request.method == 'POST':
        # 1. Actualizar los campos del objeto existente
        mensaje_a_editar.nombre = request.form['nombre']
        mensaje_a_editar.mensaje = request.form['mensaje']

        # 2. Guardar cambios (no se usa db.session.add, solo commit)
        db.session.commit()
        return redirect(url_for('ver_mensajes'))

    # 3. GET: Mostrar el formulario con los datos actuales
    return render_template('editar_mensaje.html', mensaje=mensaje_a_editar)

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# ...

# Inicializa el LoginManager después de inicializar la app (app = Flask(__name__))
login_manager = LoginManager()
login_manager.init_app(app)

# Ruta a la que Flask-Login redirige si el usuario intenta acceder a una página protegida
login_manager.login_view = 'login'

# Mensaje que se muestra si intenta acceder sin estar logueado (opcional)
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    # Método para hashear la contraseña antes de guardarla
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Método para verificar la contraseña
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Usuario('{self.username}', '{self.email}')"

# Función requerida por Flask-Login para cargar un usuario desde la ID de la sesión
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


# Ruta de Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        # Crear un nuevo usuario y hashear la contraseña
        user = Usuario(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'¡Cuenta creada para {form.username.data}! Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))  # Redirigir a la página de login

    return render_template('registro.html', form=form)


# Ruta de Inicio de Sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 1. Buscar el usuario por nombre de usuario
        user = Usuario.query.filter_by(username=form.username.data).first()

        # 2. Verificar si el usuario existe Y si la contraseña es correcta
        if user and user.check_password(form.password.data):
            # Login exitoso
            login_user(user, remember=form.remember.data)  # Usa la función de Flask-Login
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('inicio'))
        else:
            # Login fallido
            flash('Inicio de sesión fallido. Por favor revisa el usuario y la contraseña.', 'danger')

    return render_template('login.html', form=form)


# Ruta de Cierre de Sesión
@app.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    # Ejecuta el servidor en modo depuración (muestra errores y se recarga automáticamente)
    app.run(debug=True)

