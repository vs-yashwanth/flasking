from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema

bp = Blueprint('Users', __name__, description = 'Operations on users')


@bp.route('/register')
class Register(MethodView):

    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, data):
        user = UserModel(username = data['username'], 
                            password = pbkdf2_sha256.hash(data['password']))
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        
        return user
    

@bp.route('/user/<int:user_id>')
class User(MethodView):

    @bp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, str(e))
        
        return {"message": "User successfully deleted"}
