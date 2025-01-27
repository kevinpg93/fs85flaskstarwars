import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuarios, Planetas, Personajes, Favoritos_planetas, Favoritos_personajes
from sqlalchemy import select
#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#GET de todos los usuarios
@app.route('/usuarios', methods=['GET'])
def handle_hello():
    data = db.session.scalars(select(Usuarios)).all()
    results = list(map(lambda item: item.serialize(),data))
    print(results)
    response_body = {
        "msg": "Hello, this are the usuarios ",
        "results": results
    }
    return jsonify(response_body), 200
#GET de todos los planetas
@app.route('/planetas', methods=['GET'])
def handle_planetas():
    data = db.session.scalars(select(Planetas)).all()
    results = list(map(lambda item: item.serialize(),data))
    print(results)
    response_body = {
        "msg": "Hello, this are the planets ",
        "results": results
    }
    return jsonify(response_body), 200
#GET de todos los personajes
@app.route('/personajes', methods=['GET'])
def handle_personajes():
    data = db.session.scalars(select(Personajes)).all()
    results = list(map(lambda item: item.serialize(),data))
    print(results)
    response_body = {
        "msg": "Hello, this are the personajes ",
        "results": results
    }
    return jsonify(response_body), 200
#GET de los favoritos personajes
@app.route('/favoritos-personajes', methods=['GET'])
def handle_favoritos_personajes():
    data = db.session.scalars(select(Favoritos_personajes)).all()
    results = list(map(lambda item: item.serialize(),data))
    print(results)
    response_body = {
        "msg": "Hello, this are the favoritos ",
        "results": results
    }
    return jsonify(response_body), 200
#GET de los favoritos planetas
@app.route('/favoritos-planetas', methods=['GET'])
def handle_favoritos_planetas():
    data = db.session.scalars(select(Favoritos_planetas)).all()
    results = list(map(lambda item: item.serialize(),data))
    print(results)
    response_body = {
        "msg": "Hello, this are the favoritos ",
        "results": results
    }
    return jsonify(response_body), 200
#GET de un usuario unico
@app.route('/usuario/<int:id>', methods=['GET'])
def traer_usuario(id):
    usuario = db.session.execute(select(Usuarios).filter_by(id=id)).scalar_one()
    response_body = {
        "msg": "Hello, this is your GET /user response ",
        "result":usuario.serialize()
    }
    return jsonify(response_body), 200
#GET de un planeta unico
@app.route('/planeta/<int:id>', methods=['GET'])
def traer_planeta(id):
    planeta = db.session.execute(select(Planetas).filter_by(id=id)).scalar_one()
    response_body = {
        "msg": "Hello, this is your planeta ",
        "result":planeta.serialize()
    }
    return jsonify(response_body), 200
#GET de un personaje unico
@app.route('/personaje/<int:id>', methods=['GET'])
def traer_personaje(id):
    personaje = db.session.execute(select(Personajes).filter_by(id=id)).scalar_one()
    response_body = {
        "msg": "Hello, this is your personaje ",
        "result":personaje.serialize()
    }
    return jsonify(response_body), 200
#GET de un favorito unico
@app.route('/favorito-personaje/<int:id>', methods=['GET'])
def traer_personaje_favorito(id):
    favorito = db.session.execute(select(Favoritos_personajes).filter_by(id=id)).scalar_one()
    response_body = {
        "msg": "Hello, this is your favorito ",
        "result":favorito.serialize()
    }
    return jsonify(response_body), 200
#Metodo POST para crear un usuario, envio los datos a la base de datos
@app.route('/usuario', methods=['POST'])
def crear_usuario():
    request_data = request.json
    usuario = Usuarios(correo=request_data["correo"], contraseña=request_data["contraseña"])
    db.session.add(usuario)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your usuario ",
        "result":request_data
    }
    return jsonify(response_body), 200
#Metodo POST para crear un planeta, envio los datos a la base de datos
@app.route('/planeta', methods=['POST'])
def crear_planeta():
    request_data = request.json
    planeta= Planetas(nombre_planeta=request_data["nombre_planeta"], poblacion=request_data["poblacion"], extension=request_data["extension"])
    db.session.add(planeta)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your new planeta ",
        "result":request_data
    }
    return jsonify(response_body), 200
#Metodo POST para crear un personaje, envio los datos a la base de datos
@app.route('/personaje', methods=['POST'])
def crear_personaje():
    request_data = request.json
    personaje= Personajes(nombre_personaje=request_data["nombre_personaje"], color_de_ojos=request_data["color_de_ojos"], color_de_pelo=request_data["color_de_pelo"])
    db.session.add(personaje)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your new personaje ",
        "result":request_data
    }
    return jsonify(response_body), 200
#POST favoritos, agregar planeta a favorito
@app.route('/favoritos-planeta', methods=['POST'])
def crear_planeta_favorito():
    request_data = request.json
    planeta_favorito= Favoritos_planetas(planeta_id=request_data["planeta_id"], usuario_id=request_data["usuario_id"])
    db.session.add(planeta_favorito)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your planeta favorito ",
        "result":request_data
    }
    return jsonify(response_body), 200
#POST favoritos, agregar personaje a favorito
@app.route('/favoritos-personaje', methods=['POST'])
def crear_personaje_favorito():
    request_data = request.json
    personaje_favorito= Favoritos_personajes(personaje_id=request_data["personaje_id"], usuario_id=request_data["usuario_id"])
    db.session.add(personaje_favorito)
    db.session.commit()
    response_body = {
        "msg": "Hello, this is your personaje favorito ",
        "result":request_data
    }
    return jsonify(response_body), 200
#Metodo DELETE de un usuario
@app.route('/usuario/<int:id>', methods=['DELETE'])
def borrar_usuario(id):
        usuario = db.session.execute(select(Usuarios).filter_by(id=id)).scalar_one_or_none() #si no eso este metodo , no puedo gestionar el not found
        if usuario is None:
            return jsonify({"msg": "Usuario not found"}), 400#error por parte de peticion
        db.session.delete(usuario)
        db.session.commit()
        response_body = {
        "msg": "Usuario eliminado"
    }
        return jsonify(response_body), 200
#Metodo delete, uso select para buscar en la tabla la id del usuarios por el id dado, el metodo .scalar_one() me da un unico resultado, o me devuelve excepcion, el db.session.delete(usuario)
#marca el usuario para ser eliminado en la base de datos (db, base de datos),db.session.commit() ejecuta los cambios en la base de datos, si no hago esto no funcionara
#el delete
#Metodo DELETE de un personaje
@app.route('/personaje/<int:id>', methods=['DELETE'])
def borrar_personaje(id):
        personaje = db.session.execute(select(Personajes).filter_by(id=id)).scalar_one_or_none() #si no eso este metodo , no puedo gestionar el not found
        if personaje is None:
            return jsonify({"msg": "Personaje not found"}), 400#error por parte de peticion
        db.session.delete(personaje)
        db.session.commit()
        response_body = {
        "msg": "Personaje eliminado"
    }
        return jsonify(response_body), 200
#Metodo DELETE de un planeta
@app.route('/planeta/<int:id>', methods=['DELETE'])
def borrar_planeta(id):
        planeta = db.session.execute(select(Planetas).filter_by(id=id)).scalar_one_or_none() #si no eso este metodo , no puedo gestionar el not found
        if planeta is None:
            return jsonify({"msg": "Planeta not found"}), 400#error por parte de peticion
        db.session.delete(planeta)
        db.session.commit()
        response_body = {
        "msg": "Planeta eliminado"
    }
        return jsonify(response_body), 200
#Metodo DELETE de un planeta favorito
@app.route('/favoritos-planeta/<int:id>', methods=['DELETE'])
def borrar_planeta_favorito(id):
        favorito = db.session.execute(select(Favoritos_planetas).filter_by(id=id)).scalar_one_or_none() #si no eso este metodo , no puedo gestionar el not found
        if favorito is None:
            return jsonify({"msg": "Favorito not found"}), 400#error por parte de peticion
        db.session.delete(favorito)
        db.session.commit()
        response_body = {
        "msg": "Favorito eliminado"
    }
        return jsonify(response_body), 200
#Metodo DELETE de un personaje favorito
@app.route('/favoritos-personaje/<int:id>', methods=['DELETE'])
def borrar_personaje_favorito(id):
        favorito = db.session.execute(select(Favoritos_personajes).filter_by(id=id)).scalar_one_or_none() #si no eso este metodo , no puedo gestionar el not found
        if favorito is None:
            return jsonify({"msg": "Favorito not found"}), 400#error por parte de peticion
        db.session.delete(favorito)
        db.session.commit()
        response_body = {
        "msg": "Favorito eliminado"
    }
        return jsonify(response_body), 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)