
import psycopg2
from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
bootstrap = Bootstrap(app)

class LoginForm (FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')



@app.route('/')
def index():
    return render_template('base.html')

@app.route('/login')
def login():
    login_form = LoginForm()

@app.route('/libros')
def libros():
    # Conectar con la base de datos
    conexion = psycopg2.connect(
        database="biblioteca",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conexion.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM libros_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    conexion.close()
    return render_template('libros.html', datos=datos)

@app.route('/autores')
def autores():
    # Conectar con la base de datos
    conexion = psycopg2.connect(database="biblioteca",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conexion.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM autores_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    conexion.close()
    return render_template('autores.html', datos=datos)

@app.route('/editoriales')
def editoriales():
    return 'Hola mundo'

@app.route('/paises')
def paises():
     # Conectar con la base de datos
    conexion = psycopg2.connect(
        database="biblioteca",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conexion.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM pais''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    conexion.close()
    return render_template('paises.html', datos=datos)

@app.route('/update_pais1/<int:id_pais>', methods=['POST'])
def update_pais(id_pais):
    conexion = psycopg2.connect(
        database="biblioteca",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    cursor = conexion.cursor()
    cursor.execute('''SELECT * FROM pais WHERE id_pais=%s''', id_pais)
    #recuperar la informacion
    datos = cursor.fetchall()
    id_pais = request.form['id_pais']
    nombre = request.form['nombre']
    datos = {
        'id_pais': id_pais,
        'nombre': nombre
    }
    return render_template('editar_pais.html', datos=datos)
    
@app.route('/update_pais2/<int:id_pais>')
def update_pais2(id_pais):
    conexion = psycopg2.connect(
        database="biblioteca3a",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    cursor = conexion.cursor()
    cursor.execute('''UPDATE pais SET nombre=%s WHERE id_pais=%s''', (id_pais,)) 
    conexion.commit()
    cursor.close() 
    conexion.close() 
    return redirect(url_for('index')) 


@app.route('/delete_pais/<int:id_pais>', methods=['POST'])
def delete_pais(id_pais):
    conexion = psycopg2.connect(
        database="biblioteca",
        user="postgres",
        password="gnieva",
        host="localhost",
        port="5432"
    )
    cursor = conexion.cursor()
  
    cursor.execute('''DELETE FROM pais WHERE id=%s''', (id_pais,)) 
    conexion.commit()
    cursor.close() 
    conexion.close() 
    return redirect(url_for('index')) 
