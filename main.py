import os

import psycopg2
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

import db
from flask_session import Session
from forms import LibrosForm, LoginForm

app = Flask(__name__)
# Configura las variables de entorno
app.config['FLASK_APP'] = 'main.py'
app.config['FLASK_DEBUG'] = 1

bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'SUPER SECRETO'
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)


@app.route('/')
def index():
    return render_template('base.html')

@app.errorhandler(404)
def error404(error):
    return render_template('404.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
    #if request.method == "POST":
        # Procesa el formulario de inicio de sesión aquí
        correo = request.form["correo"]
        palabra_secreta = request.form["palabra_secreta"]

        # Verifica las credenciales (solo como ejemplo)
        if correo == "admin_biblio" and palabra_secreta == "tu_contraseña":
            session["usuario"] = "admin_biblio"  # Inicia sesión
            return redirect(url_for("ruta_protegida"))
        else:
            flash("Credenciales incorrectas", "error")

    return render_template("login.html", form=login_form)  # Muestra el formulario


# @app.route('/login')
# def login():
#     login_form = LoginForm()

@app.route('/libros')
def libros():
    # Conectar con la base de datos
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM libros_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('libros.html', datos=datos)

@app.route('/insertar_libro', methods=['GET', 'POST'])
def insertar_libro():
    form = LibrosForm()

    autores = obtener_autores()
    form.fk_autor.choices = [(autor[0], f"{autor[1]} {autor[2]}") for autor in autores]
    editoriales = obtener_editoriales()
    form.fk_editorial.choices = [(editorial[0], f"{editorial[1]}") for editorial in editoriales]
   
    if form.validate_on_submit():
        # Si se dió click en el botón del form y no faltan datos
        # se recupera la información que el user escribió en el form
        titulo = form.titulo.data
        fk_autor = form.fk_autor.data
        fk_editorial = form.fk_editorial.data
        edicion = form.edicion.data
        # Insertar los datos
        conn = db.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO libro (titulo, fk_autor, fk_editorial, edicion)
                       VALUES (%s, %s, %s, %s)''', (titulo, fk_autor, fk_editorial, edicion))
        conn.commit()
        cursor.close()
        db.desconectar(conn)
        return redirect(url_for('libros'))
    return render_template('insertar_libro.html', form=form, autores=autores, editoriales=editoriales)

def obtener_autores():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM autor''')
    autores = cursor.fetchall() 
    # Crear una lista de diccionarios con los campos deseados
    lista_autores = []
    for autor in autores:
        autor_dict = {
            'id': autor[0],
            'nombre': autor[2],
            'apellido': autor[3]
        }
        lista_autores.append(autor_dict)
    cursor.close()
    db.desconectar(conn)
    return autores

def obtener_editoriales():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, nombre FROM editorial''')
    editoriales = cursor.fetchall() 
    # Crear una lista de diccionarios con los campos deseados
    lista_editoriales = []
    for editorial in editoriales:
        editorial_dict = {
            'id': editorial[0],
            'nombre': editorial[1],
        }
        lista_editoriales.append(editorial_dict)
    cursor.close()
    db.desconectar(conn)
    return editoriales

@app.route('/autores')
def autores():
    # Conectar con la base de datos
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM autores_view''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('autores.html', datos=datos)

@app.route('/editoriales')
def editoriales():
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM editoriales_view''')
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editoriales.html', datos=datos)

@app.route('/paises')
def paises():
     # Conectar con la base de datos
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # ejecutar una consulta en postgres
    cursor.execute('''SELECT * FROM pais ORDER BY id''')
    #recuperar la informacion
    datos = cursor.fetchall()
    #cerrar cursos y conexion a la base de datos
    cursor.close()
    db.desconectar(conn)
    return render_template('paises.html', datos=datos)

@app.route('/update1_pais/<int:id_pais>', methods=['POST'])
def update1_pais(id_pais):
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    # recuperar el registro del id_pais seleccionado
    cursor.execute('''SELECT * FROM pais WHERE id=%s''',
                   (id_pais,))
    datos = cursor.fetchall()
    cursor.close()
    db.desconectar(conn)
    return render_template('editar_pais.html', datos=datos)
    
@app.route('/update2_pais/<int:id_pais>', methods=['POST'])
def update2_pais(id_pais):
    nombre = request.form['nombre']
    conn = db.conectar()
    # crear un cursor (objeto para recorrer las tablas)
    cursor = conn.cursor()
    cursor.execute('''UPDATE pais SET nombre=%s WHERE id=%s''', (nombre, id_pais,))
    conn.commit()
    cursor.close()
    db.desconectar(conn)
    return redirect(url_for('index'))


@app.route('/delete_pais/<int:id_pais>', methods=['POST'])
def delete_pais(id_pais):
    conn = db.conectar()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM pais WHERE id=%s''', (id_pais,)) 
    conn.commit()
    cursor.close() 
    db.desconectar(conn)
    return redirect(url_for('index')) 
