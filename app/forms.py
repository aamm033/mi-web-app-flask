# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms import PasswordField, ValidationError

class RegistroForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()]) # Asegúrate de importar Email de wtforms.validators
    password = PasswordField('Contraseña', validators=[DataRequired()])
    # Campo de confirmación para asegurar que la contraseña se escribió correctamente
    confirm_password = PasswordField('Confirmar Contraseña',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    # Campo para "Recordarme" (opcional, pero útil)
    remember = BooleanField('Recordarme') # Asegúrate de importar BooleanField de wtforms
    submit = SubmitField('Iniciar Sesión')

# Definición del formulario de contacto
class ContactoForm(FlaskForm):
    # Reglas: Nombre es obligatorio y debe tener entre 2 y 50 caracteres
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])

    # 🟢 AÑADIR ESTE CAMPO: email
    email = StringField('Email', validators=[DataRequired(), Email()])

    # Reglas: Mensaje es obligatorio
    mensaje = TextAreaField('Mensaje', validators=[DataRequired()])

    # Botón de envío
    submit = SubmitField('Enviar Mensaje')