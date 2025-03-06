from os import access
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

from blocklist import BLOCKLIST
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
    
@bp.route('/login')
class UserLogin(MethodView):
    @bp.arguments(UserSchema)
    def post(self, data):
        user = UserModel.query.filter(UserModel.username == data['username']).first()
        if user and pbkdf2_sha256.verify(data['password'], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {'access_token': access_token, "refresh_token": refresh_token    }
        
        abort(401, message='invalid credentials')

@bp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh = False)
        return {"access_token": new_token}

@bp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "successfully logged out"}
    

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
