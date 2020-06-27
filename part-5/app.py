from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from user import UserRegister

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "kalyan"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help="This field cannot be empty!"
    )

    @jwt_required()
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
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type =float,
        #     required = True,
        #     help = "This field cannot be empty!"
        # )
        # data = Item.parser.parse_args() # parser is a class variable
        if next(filter(lambda x: x["name"] == name, items), None):
            return (
                {"message": "An item with name '{}' already exists.".format(name)},
                400,
            )
        # data = request.get_json()
        data = Item.parser.parse_args()  # parser is a class variable
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message": "Item deleted"}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type =float,
        #     required = True,
        #     help = "This field cannot be empty!"
        # )
        data = parser.parse_args()  # parser is a class variable
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")  # http://127.0.0.1:5000/item/some_name
api.add_resource(ItemList, "/items")  # http://127.0.0.1:5000/items
api.add_resource(UserRegister, "/register")

app.run(port=5000, debug=True)
