from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
# app is needed for routes
# Api works with resources and every resource needs to be a class
api = Api(app)

items = []


class Item(Resource):

    def get(self, name):
        for item in items:
            if name == item['name']:
                return item
        return {'item': None}, 404

    def post(self, name):
        item = {'name': name, 'price': 12.01}
        items.append(item)
        return item, 201


class ItemList(Resource):

    def get(self):
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')  # http://127.0.0.1:5000/item/cake
api.add_resource(ItemList, '/items')  # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
