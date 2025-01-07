from flask import Flask

app = Flask(__name__)

stores = [
    {
        'name': 'My Wonderful Store',
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

@app.get('/store')
def get_stores():
    return {'stores': stores}