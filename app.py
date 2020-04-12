from flask import Flask, jsonify, request, render_template

app = Flask(__name__)  # __name__ gives the app a unique name
stores = [
    {
        'name': 'My lovely store',
        'items': [
            {
                'name': 'Döner',
                'price': 3.5
            }
        ]
    }
]


# For backend POV
# POST - receive data
# GET - send data back only

@app.route('/')
def home():
    return render_template('index.html')

# POST - /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    new_request = request.get_json()
    new_store = {
        'name': new_request['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET - /store/<string:name>
@app.route('/store/<string:name>')  # 'http://127.0.0.1:5000/store/any_name'
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message': 'Something went wrong!'})

# GET - /store
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

# POST - /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if name == store['name']:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message': 'Something went wrong!'})

# GET - /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'message': 'Something went wrong!'})


app.run(port=5000)
