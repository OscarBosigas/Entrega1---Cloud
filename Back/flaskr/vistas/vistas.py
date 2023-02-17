from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from ..modelos import *

usaurioSchema = UsuarioSchema()

class SignIn(Resource):
    def post(self):
            nuevo_usuario = Usuarios(nombre=request.json["nombre"], correo=request.json["correo"], contrasena=request.json["contrasena"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            return {'menaje':'Usuario creado'}

class LogIn(Resource):
    def post(self):
        u_correo = request.json["correo"]
        u_contrasena = request.json["contrasena"]
        usuario = Usuarios.query.filter_by(correo=u_correo, contrasena=u_contrasena).first()
        token_de_Acceso = create_access_token(identity=request.json["correo"])
        if usuario:
            return {'mensaje':'Inicio de sesion','token_de_acceso':token_de_Acceso}, 200
        else:
            return {'mensaje':'Usuario no encontrado'}, 400
        