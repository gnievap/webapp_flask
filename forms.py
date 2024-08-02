from flask_wtf import FlaskForm
from wtforms import (IntegerField, PasswordField, SelectField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired


class LibrosForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    fk_autor = SelectField('Autor', choices=[], validators=[DataRequired()], coerce=int)
    fk_editorial = SelectField('Editorial', choices=[], validators=[DataRequired()], coerce=int)
    edicion = IntegerField('Edicion', validators=[DataRequired()])
    submit = SubmitField('Agregar Libro')

class LoginForm(FlaskForm):
    username = StringField("Nombre de usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar sesión")