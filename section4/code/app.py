from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity


app = Flask(__name__)  # app is needed for routes
app.secret_key = 'jose'
api = Api(app)  # Api works with resources & every resource needs to be a class

app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):

    def get(self, name):
        item = next(filter(lambda it: it['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda it: it['name'] == name, items), None):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        access_token = create_access_token(identity={"name": name})
        return {"access_token": access_token}, 201


class ItemList(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/car
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
