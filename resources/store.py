import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

bp = Blueprint('stores', __name__, description='stores service')

@bp.route('/store/<string:store_id>')
class Stores(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        if store_id not in stores:
            abort(404, message='Store not found')
        return {'store': stores[store_id]}, 201

    def delete(self, store_id):
        if store_id not in stores:
            abort(404, message='Store not found')
        del stores[store_id]
        return {'message': "Successfully deleted"}, 200
    

@bp.route('/store')
class StoreList(MethodView):

    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, data):
        store_id = uuid.uuid4().hex
        new_store = {**data, 'id': store_id}
        stores[store_id] = new_store
        return new_store, 201