import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

bp = Blueprint('items', __name__, description="items service")

@bp.route('/item/<string:item_id>')
class Item(MethodView):
    def get(self, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        return items[item_id], 200

    def put(self, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        data = request.get_json()
        items[item_id] = {**items[item_id], **data}
        return items[item_id], 200

    def delete(self, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        del items[item_id]
        return {'message': 'Successfully deleted'}, 200

    
@bp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {'items': list(items.values())}, 200

    def post(self):
        data = request.get_json()
        if data['store_id'] not in stores:
            abort(404, message='Store not found')
        item_id = uuid.uuid4().hex
        new_item = {**data, 'id': item_id}
        items[item_id] = new_item
        
        return {'item': new_item}, 201