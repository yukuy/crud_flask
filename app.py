from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login_flask'

# Inicializar MySQL
mysql = MySQL(app)

# Ruta para la página principal
@app.route('/')
def index():
    if 'user_id' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute('SELECT * FROM usuarios')
        users = cursor.fetchall()
        return render_template('index.html', user=user, users=users)
    return redirect(url_for('login'))

# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        foto = None
        
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':
                foto = foto_file.filename
                foto_path = os.path.join('static/uploads', foto)
                foto_file.save(foto_path)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO usuarios (nombre, correo, clave, foto) VALUES (%s, %s, %s, %s)', (nombre, correo, clave, foto))
        mysql.connection.commit()
        
        flash('Registro exitoso!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        clave = request.form['clave']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE correo = %s AND clave = %s', (correo, clave))
        user = cursor.fetchone()
        
        if user:
            session['user_id'] = user['id']
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o clave incorrectos', 'danger')
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Ruta para agregar usuario
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        foto = None
        
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':
                foto = foto_file.filename
                foto_path = os.path.join('static/uploads', foto)
                foto_file.save(foto_path)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO usuarios (nombre, correo, clave, foto) VALUES (%s, %s, %s, %s)', (nombre, correo, clave, foto))
        mysql.connection.commit()
        
        flash('Usuario agregado exitosamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_user.html')

# Ruta para editar usuario
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id,))
    user = cursor.fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        clave = request.form['clave']
        
        # Manejo del archivo de foto
        foto = user['foto']
        if 'foto' in request.files:
            foto_file = request.files['foto']
            if foto_file.filename != '':
                foto = foto_file.filename
                foto_path = os.path.join('static/uploads', foto)
                foto_file.save(foto_path)
        
        cursor.execute("""
            UPDATE usuarios
            SET nombre = %s, correo = %s, clave = %s, foto = %s
            WHERE id = %s
        """, (nombre, correo, clave, foto, id))
        mysql.connection.commit()
        flash('Usuario actualizado correctamente!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_user.html', user=user)

# Ruta para eliminar usuario
@app.route('/delete/<int:id>')
def delete_user(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM usuarios WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
