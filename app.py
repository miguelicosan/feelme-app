from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Response
import bcrypt  # Para hashear las contraseñas
from config import app, usuarios



# Routes
@app.route('/')
def login():
    return render_template('/login.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@app.route('/login', methods=['POST'])
def authenticate():
    print("*************** authenticate")
    if request.method == 'POST':
        email_usuario = usuarios.find_one({'email': request.form['email']})
        print("*************** authenticate email_usuario: ", email_usuario)

        if email_usuario:
            if bcrypt.hashpw(request.form['password'].encode('utf-8'), email_usuario['password'].encode('utf-8')) == email_usuario['password'].encode('utf-8'):
                session['username'] = request.form['username']
                # Encontramos el usuario
                response = {
                    'status': 'success',
                    'message': 'Usuario autenticado exitosamente'
                }
                
                return response, redirect(url_for('index'))

        response = {
            'status': 'error',
            'message': 'Usuario y/o contraseña incorrectos'
        }
        # flash('Combinación de usuario y contraseña incorrecta')
        
        
        return response, render_template('login.html')

    return render_template('login')

@app.route('/forgot_password.html')
def forgot_password():
    print("forgot_password")
    return render_template('forgot_password.html')

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Obtener los datos del formulario
        usuario = request.form['usuario']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        email = request.form['email']
        password = request.form['password']
        edad = request.form['edad']
        sexo = request.form['sexo']
        peso = request.form['peso']
        altura = request.form['altura'] 

        # Hashear la contraseña antes de almacenarla en la base de datos
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Crear un nuevo usuario en MongoDB
        new_user = {
            'usuario': usuario,
            'nombre': nombre,
            'apellidos': apellidos,
            'email': email,
            'password': hashed_password,
            'edad': edad,
            'sexo': sexo,
            'peso': peso,
            'altura': altura,
            'confirmado': "false" # El usuario no ha confirmado su correo electrónico
        }

        # Insertar el nuevo usuario en la colección
        try:
            usuarios.insert_one(new_user)
        except Exception as e:
            print(e)
            return 'Hubo un error al crear el usuario'

        # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
