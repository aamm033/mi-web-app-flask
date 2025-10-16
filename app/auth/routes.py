# app/auth/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db  # Importación del objeto db creado en __init__.py
from app.models import Usuario
from app.forms import RegistroForm, LoginForm, PerfilForm, CambiarContrasenaForm

# Crea el Blueprint
auth = Blueprint('auth', __name__)



# RUTAS EXISTENTES (REGISTRO Y LOGIN)


@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    # ... (código de registro existente) ...
    if form.validate_on_submit():
        # ... (lógica de creación de usuario) ...
        usuario_nuevo = Usuario(
            username=form.username.data,
            email=form.email.data,
        )
        usuario_nuevo.set_password(form.password.data)
        try:
            db.session.add(usuario_nuevo)
            db.session.commit()
            flash(f'¡Cuenta creada para {form.username.data}! Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la cuenta. El usuario o correo electrónico ya existen.', 'danger')
            print(f"Error de DB en registro: {e}")
    return render_template('registro.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # ... (código de login existente) ...
    if form.validate_on_submit():
        user = Usuario.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')

            # 💡 CAMBIO DE MEJORA: Redirigir a 'perfil' si el login fue directo
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('auth.perfil'))  # ⬅️ Redirigir a la nueva página de perfil
        else:
            flash('Inicio de sesión fallido. Usuario o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))



# 🟢 NUEVAS RUTAS DE PERFIL Y CONFIGURACIÓN


@auth.route('/perfil', methods=['GET', 'POST'])
@login_required  # ⬅️ Solo accesible si el usuario está logueado
def perfil():
    # Carga la información actual del usuario en el formulario
    perfil_form = PerfilForm(obj=current_user)

    if perfil_form.validate_on_submit():
        # Lógica para actualizar el campo 'nombre'
        current_user.nombre = perfil_form.nombre.data
        db.session.commit()
        flash('¡Tu perfil ha sido actualizado!', 'success')
        return redirect(url_for('auth.perfil'))

    # Renderiza la plantilla, pasando el formulario
    return render_template(
        'perfil.html',
        perfil_form=perfil_form,
        # Se puede pasar el formulario de cambio de contraseña aquí también,
        # pero para simplicidad, usamos una ruta separada.
    )


@auth.route('/cambiar_contrasena', methods=['GET', 'POST'])
@login_required  # ⬅️ Solo accesible si el usuario está logueado
def cambiar_contrasena():
    contrasena_form = CambiarContrasenaForm()

    if contrasena_form.validate_on_submit():
        # 1. Verificar que la contraseña actual sea correcta
        if not current_user.check_password(contrasena_form.contrasena_actual.data):
            flash('La contraseña actual es incorrecta.', 'danger')
            return redirect(url_for('auth.cambiar_contrasena'))

        # 2. La contraseña actual es correcta, establecemos la nueva
        # Utilizamos la función del modelo que hashea la contraseña
        current_user.set_password(contrasena_form.contrasena_nueva.data)
        db.session.commit()

        flash('¡Tu contraseña ha sido cambiada exitosamente!', 'success')
        # Redirigir de nuevo a la página de perfil
        return redirect(url_for('auth.perfil'))

    return render_template('cambiar_contrasena.html', contrasena_form=contrasena_form)