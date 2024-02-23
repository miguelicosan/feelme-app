
from flask import Flask
from flask_pymongo import PyMongo
import secrets

###########################################
#          MongoDB Configuration          #
###########################################
# Usuario y contraseña que pondremos en variables de entorno
app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/feelchat_db"
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
mongo = PyMongo(app)

try:
    usuarios = mongo.db.usuarios  # Colección de usuarios
    print(usuarios.find_one())  # Comprobamos que la conexión a la base de datos es correcta
    
except Exception as e:
    print("[MONGO DB]: ", e)