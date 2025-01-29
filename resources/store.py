import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("stores", __name__, description='Operations on stores')

@blp.route('/store/<string:store_id>')
class Store(MethodView):
    def get(self, store_id):
        if store_id not in stores:
            abort(404, message='Store not found')
        return {'store': stores[store_id]}, 201

    def delete(self, store_id):
        if store_id not in stores:
            abort(404, message='Store not found')
        del stores[store_id]
        return {'message': "Successfully deleted"}, 200
