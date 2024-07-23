from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired


class LibrosForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    fk_autor = SelectField('Autor', choices=[], validators=[DataRequired()], coerce=int)
    fk_editorial=IntegerField('Editorial ID', validators=[DataRequired()])
    edicion = IntegerField('Edicion', validators=[DataRequired()])
    submit = SubmitField('Agregar Libro')