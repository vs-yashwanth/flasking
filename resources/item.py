import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.item import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError

bp = Blueprint('items', __name__, description="items service")

@bp.route('/item/<string:item_id>')
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.price = data['price']
            item.name = data['name']
        else:
            item = ItemModel(**data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='Error occurred while modifying the item')
        
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {'message': 'Item deleted successfully'}    


    
@bp.route('/item')
class ItemList(MethodView):

    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, data):
        
        item = ItemModel(**data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message='An error occurred while inserting the item')

        
        return item, 201