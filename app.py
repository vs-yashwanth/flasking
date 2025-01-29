import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello Flask store!'

# stores
@app.get('/stores')
def get_stores():
    return {'stores': list(stores.values())}

@app.post('/store')
def create_store():
    data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**data, 'id': store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.get('/store/<string:store_id>')
def get_store(store_id):
    if store_id not in stores:
        abort(404, message='Store not found')
    return {'store': stores[store_id]}, 201

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    if store_id not in stores:
        abort(404, message='Store not found')
    del stores[store_id]
    return {'message': "Successfully deleted"}, 200

# items
@app.get('/items')
def get_items():
    return {'items': list(items.values())}, 200

@app.post('/item')
def create_item():
    data = request.get_json()
    if data['store_id'] not in stores:
        abort(404, message='Store not found')
    item_id = uuid.uuid4().hex
    new_item = {**data, 'id': item_id}
    items[item_id] = new_item
    
    return {'item': new_item}, 201

@app.get('/item/<string:item_id>')
def get_item(item_id):
    if item_id not in items:
        abort(404, message='Item not found')
    return items[item_id], 200

@app.put('/item/<string:item_id>')
def update_item(item_id):
    if item_id not in items:
        abort(404, message='Item not found')
    data = request.get_json()
    items[item_id] = {**items[item_id], **data}
    return items[item_id], 200

 
@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    if item_id not in items:
        abort(404, message='Item not found')
    del items[item_id]
    return {'message': 'Successfully deleted'}, 200
    