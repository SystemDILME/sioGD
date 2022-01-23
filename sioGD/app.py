"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
# Llamamos Flask
from flask import Flask, render_template, request, redirect, url_for, flash, session
# Lamamos a SQL desde el entorno flask_mysqldb
from flask_mysqldb import MySQL
#entorno para encriptación de password
#import bcrypt 

# Configuración App
app = Flask(__name__)

#Configuro llave secreta
app.secret_key='appLogin'
# Salt para encriptamiento
#salt = bcrypt.gentsalt()
#Conexión SQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'AdminD1lm3'
app.config['MYSQL_DB'] = 'siogd'
mysql = MySQL(app)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

#Cada que un usuario entre a la raiz sera dirigido a esta dirección
@app.route('/')
def home():
    """Renders a sample page."""
    if 'user' in session:
        return render_template('users.html')
    else:  return render_template('login.html')

    #Pagina Login
@app.route('/login', methods=['POST', 'GET'])
def  login():
    if request.method == 'POST, GET':
        if 'user' in session:
            return render_template('users.html')

    else:
            user = request.form['user']
            password = request.form['password']
            session = 'user'
            session = 'password'
            cur = mysql.connection.cursor()
            sQuery = 'SELECT user, password FROM users WHERE user = %s'
            cur.execute(sQuery, [user])
            user = cur.fetchone()
            cur.close()
            return redirect(url_for('form'))
    
#configuración de usuarios
@app.route('/users', methods=['POST'])
def users():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        print (user)
        print (password)
        #ejecutamos la conexion
        cur = mysql.connection.cursor()
        # escribimos la consulta
        cur.execute('INSERT INTO users (user, password) VALUES (%s, %s)', (user, password))
        #ejecutamos la consulta
        mysql.connection.commit()
        return redirect(url_for('form'))

#Pagina llamada reportes
@app.route('/form')
def  form():
    return render_template('users.html')

# Esto sirve para correr el programa en el local host en un puerto aleatorio disponible.
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
