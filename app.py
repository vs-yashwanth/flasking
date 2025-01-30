import uuid
from flask import Flask, request
from flask_smorest import abort, Api
from db import stores, items

from resources.item import bp as item_bp
from resources.store import bp as store_bp

app = Flask(__name__)

app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['API_TITLE'] = 'Stores api'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.3'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

@app.route('/')
def home():
    return 'Hello Flask!'
    
api = Api(app)
api.register_blueprint(store_bp)
api.register_blueprint(item_bp)