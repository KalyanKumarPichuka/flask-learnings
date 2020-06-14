from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'kalyan'
api = Api(app)

items = []


class Item(Resource):
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        # item = list(filter(lambda x: x['name'] == name, items)) # if there are multiple matching items
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        # data = request.get_json(force=True) #shouldnt be used as doesnt look at conetnt-type
        # data = request.get_json(silent=True) #this gives none of content type is different
        if next(filter(lambda x: x["name"] == name, items), None):
            return (
                {"message": "An item with name '{}' already exists.".format(name)},
                400,
            )
        data = request.get_json()
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/some_name
api.add_resource(ItemList, "/items")  # http://127.0.0.1:5000/items

app.run(port=5000, debug=True)
