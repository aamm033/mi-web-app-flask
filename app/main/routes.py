# app/main/routes.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db # Importación del objeto db creado en __init__.py
from app.models import Mensaje
from app.forms import ContactoForm # Asume que forms.py está en app/

# Crea el Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/inicio')
def inicio():
    return render_template('index.html')

@main.route('/contacto', methods=['GET', 'POST'])
def contacto():
    form = ContactoForm()

    if form.validate_on_submit():
        # 🟢 VERIFICAR: USO DEL MODELO Y LA SESIÓN DE DB
        nuevo_mensaje = Mensaje(
            nombre=form.nombre.data,
            mensaje=form.mensaje.data
            # Si usas la columna 'fecha', asegúrate de que se importe `datetime` en `app/models.py`
        )
        db.session.add(nuevo_mensaje)
        db.session.commit()  # <--- CRUCIAL: ¿Estás ejecutando el commit?

        flash('¡Gracias! Tu mensaje ha sido enviado con éxito.', 'success')
        return redirect(url_for('main.contacto'))

    return render_template('contacto.html', form=form)


@main.route('/mensajes')
@login_required
def ver_mensajes():
        # 🟢 COMPROBACIÓN DE PERMISOS: Solo si es administrador
        if not current_user.is_admin:
            flash('No tienes permiso para ver esta página.', 'danger')
            return redirect(url_for('main.contacto'))

        todos_los_mensajes = Mensaje.query.all()
        return render_template('mensajes.html', mensajes=todos_los_mensajes)

@main.route('/mensaje/eliminar/<int:mensaje_id>', methods=['POST'])
@login_required
def eliminar_mensaje(mensaje_id):
    # 🟢 COMPROBACIÓN DE PERMISOS: Solo si es administrador
    if not current_user.is_admin:
        abort(403) # Error 403: Prohibido
    # 1. Buscar el mensaje por ID o devolver 404 si no existe
    mensaje_a_eliminar = Mensaje.query.get_or_404(mensaje_id)

    # 2. Borrar y guardar (commit)
    db.session.delete(mensaje_a_eliminar)
    db.session.commit()

    # 3. Redirigir de vuelta a la lista de mensajes
    return redirect(url_for('main.ver_mensajes'))

@main.route('/mensaje/editar/<int:mensaje_id>', methods=['GET', 'POST'])
def editar_mensaje(mensaje_id):
    mensaje_a_editar = Mensaje.query.get_or_404(mensaje_id)

    if request.method == 'POST':
        # 1. Actualizar los campos del objeto existente
        mensaje_a_editar.nombre = request.form['nombre']
        mensaje_a_editar.mensaje = request.form['mensaje']

        # 2. Guardar cambios (no se usa db.session.add, solo commit)
        db.session.commit()
        return redirect(url_for('main.ver_mensajes'))

    # 3. GET: Mostrar el formulario con los datos actuales
    return render_template('editar_mensaje.html', mensaje=mensaje_a_editar)

# Crea la ruta 'acerca' en tu Blueprint 'main'
@main.route('/acerca')
def acerca():
    # Renderiza la nueva plantilla acerca.html
    return render_template('acerca.html')