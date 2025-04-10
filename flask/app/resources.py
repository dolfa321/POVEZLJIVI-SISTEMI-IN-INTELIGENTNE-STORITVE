from flask import request
from flask_restful import Resource
from .models import Item
from . import db

class ItemListResource(Resource):
    def get(self):
        items = Item.query.all()
        return [item.to_dict() for item in items], 200

    def post(self):
        data = request.json
        item = Item(name=data['name'], description=data.get('description', ''))
        db.session.add(item)
        db.session.commit()
        return item.to_dict(), 201

class ItemResource(Resource):
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item.to_dict(), 200

    def put(self, item_id):
        item = Item.query.get_or_404(item_id)
        data = request.json
        item.name = data['name']
        item.description = data.get('description', '')
        db.session.commit()
        return item.to_dict(), 200

    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return '', 204
