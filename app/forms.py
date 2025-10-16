# forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    PasswordField,
    BooleanField,
    ValidationError
)
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional


class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')


# ----------------------------------------------------------------------------------

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')


# ----------------------------------------------------------------------------------

class ContactoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])
    submit = SubmitField('Enviar Mensaje')


# ----------------------------------------------------------------------------------

## 🟢 NUEVOS FORMULARIOS PARA EL PERFIL DE USUARIO

class PerfilForm(FlaskForm):
    # Campo para el nombre real/completo (Length(max=100) debe coincidir con models.py)
    # Usamos Optional() para que el usuario pueda dejarlo vacío si lo desea
    nombre = StringField('Nombre Completo', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Actualizar Perfil')


# ----------------------------------------------------------------------------------

class CambiarContrasenaForm(FlaskForm):
    contrasena_actual = PasswordField('Contraseña Actual', validators=[DataRequired()])

    contrasena_nueva = PasswordField('Nueva Contraseña', validators=[
        DataRequired(),
        Length(min=8, message='La contraseña debe tener al menos 8 caracteres.')
    ])

    confirmar_contrasena = PasswordField('Confirmar Nueva Contraseña', validators=[
        DataRequired(),
        EqualTo('contrasena_nueva', message='Las contraseñas no coinciden.')
    ])

    submit = SubmitField('Cambiar Contraseña')