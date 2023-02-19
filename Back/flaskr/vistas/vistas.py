from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from ..modelos import *

usaurioSchema = UsuarioSchema()

class SignIn(Resource):
    def post(self):
            confirmation = request.json['password2']
            nuevo_usuario = Usuarios(nombre=request.json["username"], correo=request.json["email"], contrasena=request.json["password1"])
            if(confirmation == nuevo_usuario.contrasena):
                db.session.add(nuevo_usuario)
                db.session.commit()
                return {'menaje':'Usuario creado'}
            return {'mensaje':'Error en la autenticacion'} 
            
            

class LogIn(Resource):
    def post(self):
        u_user = request.json["username"]
        u_contrasena = request.json["password"]
        usuario = Usuarios.query.filter_by(nombre=u_user, contrasena=u_contrasena).first()
        token_de_Acceso = create_access_token(identity=request.json["username"])
        if usuario:
            return {'mensaje':'Inicio de sesion','token_de_acceso':token_de_Acceso}, 200
        else:
            return {'mensaje':'Usuario no encontrado'}, 400
        