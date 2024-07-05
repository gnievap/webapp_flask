import psycopg2
from flask import Flask, redirect, render_template
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
    #return 'Hello World'
    return render_template('base.html')

@app.route('/login')
def login():
    login_form = LoginForm()

@app.route('/libros')
def libros():
    # Connect to the database 
    conn = psycopg2.connect(database="flask_db", 
                            user="postgres", 
                            password="root", 
                            host="localhost", port="5432") 
  
    # create a cursor 
    cur = conn.cursor() 
  
    # Select all products from the table 
    cur.execute('''SELECT * FROM libros''') 
  
    # Fetch the data 
    data = cur.fetchall() 
  
    # close the cursor and connection 
    cur.close() 
    conn.close() 
  
    return render_template('libros.html', data=data) 
  