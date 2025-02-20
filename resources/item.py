import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema

bp = Blueprint('items', __name__, description="items service")

@bp.route('/item/<string:item_id>')
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        return items[item_id], 200

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, data, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        items[item_id] = {**items[item_id], **data}
        return items[item_id], 200

    def delete(self, item_id):
        if item_id not in items:
            abort(404, message='Item not found')
        del items[item_id]
        return {'message': 'Successfully deleted'}, 200

    
@bp.route('/item')
class ItemList(MethodView):

    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, data):
        if data['store_id'] not in stores:
            abort(404, message='Store not found')
        item_id = uuid.uuid4().hex
        new_item = {**data, 'id': item_id}
        items[item_id] = new_item
        
        return {'item': new_item}, 201