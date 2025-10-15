# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from app import db # Importación del objeto db creado en __init__.py
from app.models import Usuario
from app.forms import RegistroForm, LoginForm # Asume que forms.py está en app/

# Crea el Blueprint
auth = Blueprint('auth', __name__)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()

    if form.validate_on_submit():
        # 🟢 1. Crear el nuevo usuario
        usuario_nuevo = Usuario(
            username=form.username.data,
            email=form.email.data,
            # 💡 El campo is_admin es False por defecto (si lo agregaste en models.py)
        )

        # 🟢 2. Hashear y establecer la contraseña
        usuario_nuevo.set_password(form.password.data)

        # 🟢 3. Guardar en la DB
        try:
            db.session.add(usuario_nuevo)
            db.session.commit()

            # 🟢 4. Mensaje de éxito y redirección
            flash(f'¡Cuenta creada para {form.username.data}! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

        except Exception as e:
            db.session.rollback()
            # 💡 Mensaje de error si el nombre de usuario/email ya existe (UNIQUE constraint)
            flash('Error al crear la cuenta. El usuario o correo electrónico ya existen.', 'danger')
            print(f"Error de DB en registro: {e}")
            # Caemos a la línea final para re-renderizar el formulario con el mensaje de error.

    return render_template('registro.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            # Login exitoso
            login_user(user, remember=form.remember.data)
            flash('¡Inicio de sesión exitoso!', 'success')

            # Obtener el parámetro 'next'. Si no existe, es None.
            next_page = request.args.get('next')

            # 🟢 LÓGICA REFORZADA:
            # Si hay un parámetro 'next', redirigir allí.
            if next_page:
                return redirect(next_page)
            else:
                # Si NO hay un parámetro 'next' (acceso directo a /login),
                # forzar la redirección al propio endpoint de login.
                return redirect(url_for('auth.login'))
        else:
            # Login fallido
            flash('Inicio de sesión fallido. Usuario o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    # 🟢 CAMBIO CRUCIAL AQUÍ: Redirigir a la página de LOGIN
    # El usuario ve el mensaje en la página de login, que es el estado que corresponde.
    return redirect(url_for('auth.login'))