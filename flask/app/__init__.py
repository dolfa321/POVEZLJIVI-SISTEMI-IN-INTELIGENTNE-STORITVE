from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from .upload import upload_bp

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

    # app.register_blueprint(upload_bp)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.register_blueprint(upload_bp)
    return app
