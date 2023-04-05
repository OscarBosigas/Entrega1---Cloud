from flask import Flask
def create_app(config_name):
    app= Flask(__name__)
    app.config['JWT_SECRET_KEY']='frase-secreta'
    app.config['PROPAGATE_EXCEPTIONS']=True
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:a123@172.17.0.1/entrega1-db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    return app
