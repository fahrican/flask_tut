from flask import Flask

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

# POST - /store data: {name:}
@app.route('/store', methods=['POST'])
def create_store():
    pass

# GET - /store/<string:name>
@app.route('/store/<string:name>')  # 'http://127.0.0.1:5000/store/any_name'
def get_store(name):
    pass

# GET - /store
@app.route('/store')
def get_stores():
    pass

# POST - /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

# GET - /store/<string:name>/item
@app.route('/store/<string:name>/item')
def get_items_in_store(name):
    pass


app.run(port=5000)
