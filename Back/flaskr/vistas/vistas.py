from flask_restful import Resource
from flask import request,  request, send_file
from flask_jwt_extended import jwt_required, create_access_token
from ..modelos import *
import zipfile
import rarfile
#from pylzma import compress
import tarfile
import os

usaurioSchema = UsersSchema()
taskSchema = TasksSchema()

class SignIn(Resource):
    def post(self):
            confirmation = request.json['password2']
            nuevo_usuario = Users(name=request.json["username"], email=request.json["email"], password=request.json["password1"])
            if(confirmation == nuevo_usuario.password):
                db.session.add(nuevo_usuario)
                db.session.commit()
                return {'menaje':'Usuario creado'}
            return {'mensaje':'Error en la autenticacion'} 
            
            

class LogIn(Resource):
    def post(self):
        u_user = request.json["username"]
        u_contrasena = request.json["password"]
        usuario = Users.query.filter_by(name=u_user, password=u_contrasena).first()
        token_de_Acceso = create_access_token(identity=request.json["username"])
        if usuario:
            return {'mensaje':'Inicio de sesion','token_de_acceso':token_de_Acceso}, 200
        else:
            return {'mensaje':'Usuario no encontrado'}, 400
        
class CompressZip(Resource):
    def post(self):
        # Obtener los archivos enviados desde el formulario
        files = request.files.getlist('file')
        # Crear un objeto ZipFile
        zip_obj = zipfile.ZipFile('archivos_comprimidos.zip', 'w', zipfile.ZIP_DEFLATED)
        # Iterar sobre cada archivo y agregarlo al objeto ZipFile
        for file in files:
            filename = file.filename
            file.save(filename)
            zip_obj.write(filename)
            os.remove(filename)
        # Cerrar el objeto ZipFile
        zip_obj.close()
        # Enviar el archivo comprimido al cliente
        ##return send_file('archivos_comprimidos.zip', as_attachment=True)
        zip_obj_path = os.path.join('compressed', 'archivos_comprimidos.zip')
        os.makedirs(os.path.dirname(zip_obj_path), exist_ok=True)
        os.rename('archivos_comprimidos.zip', zip_obj_path)
        return {'mensaje':'comprimido correctamente'}
    
class CompressRar(Resource):
    def post(self):
         # Obtener los archivos enviados desde el formulario
        files = request.files.getlist('files')
        # Crear un objeto RarFile
        rar_obj = rarfile.RarFile('archivo_comprimido.rar', mode='w')
        # Agregar los archivos al objeto RarFile
        for file in files:
            rar_obj.write(file.filename)
        # Cerrar el objeto RarFile
        rar_obj.close()
        # Guardar el archivo comprimido en una carpeta local en el servidor
        rar_obj_path = os.path.join('compressed', 'archivo_comprimido.rar')
        os.makedirs(os.path.dirname(rar_obj_path), exist_ok=True)
        os.rename('archivo_comprimido.rar', rar_obj_path)
        return {'mensaje':'comprimido correctamente'}

class Compress7Z(Resource):
    def post(self):
        # Obtener el archivo a comprimir del cuerpo de la solicitud
        file = request.files['file']
        # Leer el contenido del archivo
        content = file.read()
        # Comprimir el contenido del archivo
        compressed_content = compress(content)
        # Escribir el contenido comprimido en un nuevo archivo
        with open('compressed_file.7z', 'wb') as f:
            f.write(compressed_content)
        return {'mensaje':'comprimido correctamente'}
    

class CompressTar(Resource):
    def post(self):
        files = request.files.getlist('file')
        # Crear un archivo TAR vacío
        with tarfile.open('compressed_file.tar', 'w') as tar:
            # Agregar cada archivo al archivo TAR
            for file in files:
                # Guardar el archivo en el sistema de archivos temporal
                file.save(file.filename)
                # Agregar el archivo al archivo TAR
                tar.add(file.filename)
        # Eliminar los archivos temporales
        for file in files:
            os.remove(file.filename)
        
        return {'mensaje':'comprimido correctamente'}
    

class GetTasks(Resource):
    def get(self):
        return [taskSchema.dump(evento) for evento in Tasks.query.all()]