from flask import jsonify, request, Blueprint
from Plataforma.utils import ahora

urls_api = Blueprint('api', __name__)

@urls_api.route('/api/users', methods=["GET"])
def get_users():
    from Plataforma.models import Usuarios
    users = [user.serialize() for user in Usuarios.query.all() ]
    return jsonify(users)

@urls_api.route('/api/users/<id>', methods=["GET"])
def get_user(id):
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no existe (GET)"})
    return jsonify(user.serialize())

@urls_api.route('/api/users', methods=["POST"])
def crear_user():
    from Plataforma.app import db
    json = request.get_json(force=True)
    if json.get('username') is None or json.get('contrasena') is None:
        return jsonify({'Error': 'Bad request'}), 400
    from Plataforma.models import Usuarios
    username = json.get('username')
    contrasena = json.get('contrasena')
    nombre = json.get('nombre')
    apellidos = json.get('apellidos')
    email = json.get('email')
    nuevo = Usuarios()
    nuevo.username = username
    nuevo.contrasena = contrasena
    nuevo.nombre = nombre
    nuevo.apellidos = apellidos
    nuevo.email = email
    nuevo.admin = False
    nuevo.creacion = ahora()
    # nuevo.creado_por = current_user.username
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.serialize())

@urls_api.route('/api/users/<id>', methods=['PUT'])
def update_user(id):
    from Plataforma.app import db
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no existe (PUT)"})
    json = request.get_json(force=True)
    nombre = json.get('nombre')
    apellidos = json.get('apellidos')
    email = json.get('email')
    if nombre is None or nombre == "":
        return jsonify({"Error":"En el nombre"})
    else:
        user.nombre = nombre
    if apellidos is None or apellidos == "":
        return jsonify({"Error":"En el apellido"})
    else:
        user.apellidos = apellidos
    if email is None or email == "":
        return jsonify({"Error":"En el email"})
    else:
        user.email = email   
    db.session.commit()
    return jsonify(user.serialize())

@urls_api.route('/api/users/<id>', methods=["DELETE"])
def delete_user(id):
    from Plataforma.app import db
    from Plataforma.models import Usuarios
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        return jsonify({"Error": "El usuario no exite (DELETE)"})
    deleted = user.serialize()
    db.session.delete(user)
    db.session.commit()
    return jsonify(deleted)