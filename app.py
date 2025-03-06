import os
from flask import Flask, jsonify, request
from flask_smorest import abort, Api
from db import db
from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST
from flask_migrate import Migrate

from resources.item import bp as item_bp
from resources.store import bp as store_bp
from resources.tag import bp as tag_bp
from resources.user import bp as user_bp

def create_app(db_url = None):

    app = Flask(__name__)

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'Stores api'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.getenv('DATABASE_URL' ,'sqlite:///data.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'yash'
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
        
    api = Api(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (jsonify({'description': 'The token has been revoked', 'error': 'token_revoked'}), 401)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin" : True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payloadJ):
        return (jsonify({"message": "The token has expired"}), 401)
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (jsonify({"message": "Signature verification failed"}), 401)
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (jsonify({"message": "Request does not contain access token"}), 401)


    api.register_blueprint(store_bp)
    api.register_blueprint(item_bp)
    api.register_blueprint(tag_bp)
    api.register_blueprint(user_bp)

    return app