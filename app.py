from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        'name': 'My Store',
        'items': [
            {
                'name': 'Chair',
                'price': 15.99
            }
        ]
    }
]

@app.route('/')
def home():
    return 'Hello Flask!'

@app.get('/stores')
def get_stores():
    return {'stores': stores}

@app.post('/store')
def create_store():
    data = request.get_json()
    new_store = {
        'name': data['name'],
        'items': []
    }
    stores.append(new_store)
    return new_store, 201

@app.post('/store/<string:name>/item')
def create_item(name):
    data = request.get_json()
    for store in stores:
        if store['name'] == name:
            store['items'].append(data)
            return store, 201
    
    return {'message':"Store not found"}, 400

@app.get('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return store, 201
    return {'message': 'Store not found'}, 404

@app.get('/store/<string:name>/items')
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return store['items'], 201
    return {'message': 'Store not found'}, 404
