from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
# app is needed for routes
# Api works with resources and every resource needs to be a class
api = Api(app)

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
        return item, 201


class ItemList(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/car
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
