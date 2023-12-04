#  Importar las herramientas
# Acceder a las herramientas para crear la app web
from flask import Flask, request, jsonify

# Para manipular la DB
from flask_sqlalchemy import SQLAlchemy 

# Módulo cors es para que me permita acceder desde el frontend al backend
from flask_cors import CORS

# Crear la app
app = Flask(__name__)

# permita acceder desde el frontend al backend
CORS(app)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://usuario:contraseña@localhost:3306/nombre_de_la_base_de_datos'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/sendero_cordoba_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 6.- Informar a la app que vamos a trabajar con SQLAlchemy
db = SQLAlchemy(app)

# 7.- Crear el modelo, entidad o la tabla

class Contactos(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(50))#confirmar si es asi el email
    asunto = db.Column(db.String(550))

    def __init__(self,nombre,email,asunto):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.email=email
        self.asunto=asunto

with app.app_context():
    db.create_all()

# 9.- Crear rutas de acceso a la app
# ("/") -> Ruta al inicio
@app.route("/")
def index():
    return f'App Web para registrar contacto'

@app.route("/registro", methods=['POST'])
def registro():
    #      <input type="text" name="nombre" id="nombre">
    # {
    #   "nombre": "Luis"
    # }
    nombre_recibido = request.json["nombre"]
    email_recibido = request.json["email"]
    asunto_recibido = request.json["asunto"]

    # ¿Cómo insertar el registro en la tabla?
    nuevo_registro = Contactos(nombre=nombre_recibido, email=email_recibido, asunto=asunto_recibido)
    db.session.add(nuevo_registro)
    db.session.commit()

    return "Solicitud via post recibida"

# Retornar todos los registros en un Json
@app.route("/contactos",  methods=['GET'])
def contactos():
    # Consultar en la tabla todos los registros
    # all_registros -> lista de objetos
    all_registros = Contactos.query.all()

    # Lista de diccionarios
    data_serializada = []
    
    for objeto in all_registros:
        data_serializada.append({"id":objeto.id, "nombre":objeto.nombre, "email":objeto.email, "asunto":objeto.asunto})

    return jsonify(data_serializada)


# Modificar un registro
@app.route('/update/<id>', methods=['PUT'])
def update(id):
    # Buscar el registro a modificar en la tabla por su id
    contacto = Contactos.query.get(id)

    # {"nombre": "Felipe"} -> input tiene el atributo name="nombre"
    nombre = request.json["nombre"]
    email=request.json['email']
    asunto=request.json['asunto']

    contacto.nombre=nombre
    contacto.email=email
    contacto.asunto=asunto

    db.session.commit()

    data_serializada = [{"id":contacto.id, "nombre":contacto.nombre, "email":contacto.email, "asunto":contacto.asunto}]
    
    return jsonify(data_serializada)

   
@app.route('/borrar/<id>', methods=['DELETE'])
def borrar(id):
    
    # Se busca a la productos por id en la DB
    contacto = Contactos.query.get(id)

    # Se elimina de la DB
    db.session.delete(contacto)
    db.session.commit()

    data_serializada = [{"id":contacto.id, "nombre":contacto.nombre, "email":contacto.email, "asunto":contacto.asunto}]

    return jsonify(data_serializada)


if __name__ == "__main__":
    app.run(debug=True)

