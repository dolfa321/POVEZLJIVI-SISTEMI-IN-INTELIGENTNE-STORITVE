from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from .retrive import retrive_bp

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .resources import ItemResource, ItemListResource
    api = Api(app)
    api.add_resource(ItemListResource, '/items')
    api.add_resource(ItemResource, '/items/<int:item_id>')


    app.register_blueprint(retrive_bp)

    return app
