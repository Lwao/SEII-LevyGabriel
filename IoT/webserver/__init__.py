from crypt import methods
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    db.init_app(app)

    from .app import auth
    app.register_blueprint(auth)

    return app

