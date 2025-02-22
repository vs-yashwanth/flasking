import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from models.store import StoreModel
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

bp = Blueprint('stores', __name__, description='stores service')

@bp.route('/store/<string:store_id>')
class Stores(MethodView):
    @bp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()

        return {'message': "Store deleted successfully"}
    

@bp.route('/store')
class StoreList(MethodView):

    @bp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


    @bp.arguments(StoreSchema)
    @bp.response(201, StoreSchema)
    def post(self, data):
        
        store = StoreModel(**data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message='Store already exists')
        except SQLAlchemyError:
            abort(500, messsage='Error occurred while adding the store')

        return store, 201