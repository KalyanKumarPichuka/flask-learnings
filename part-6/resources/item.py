import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

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
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # return {"item": item}, 200 if item else 404
        item = ItemModel.find_by_name(name)
        if item:
            #return item
            return item.json()
        return {'message': 'Item not found'}, 404


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
        # if next(filter(lambda x: x["name"] == name, items), None):
        #     return (
        #         {"message": "An item with name '{}' already exists.".format(name)},
        #         400,
        #     )
        # data = request.get_json()
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()  # parser is a class variable
        #item = {"name": name, "price": data["price"]}
        item = ItemModel(name, data['price'])
        # items.append(item)
        try:
            item.insert()
        except:
            return {'message': 'An error occurred while inserting the record'}, 500 # Internal server error
        

        return item.json(), 201


    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x["name"] != name, items))
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {"message": "Item deleted"}

    def put(self, name):
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type =float,
        #     required = True,
        #     help = "This field cannot be empty!"
        # )
        data = Item.parser.parse_args()  # parser is a class variable
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # if item is None:
        #     item = {"name": name, "price": data["price"]}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = ItemModel.find_by_name(name)
        #updated_item = {'name': name, 'price': data['price']}
        updated_item = ItemModel(name, data['price'])

        if item is None:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred while inserting the item'}, 500 # Internal server error
            
        else:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred while updating the item'}, 500 # Internal server error
            

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0], 'price': row[1]})

        connection.close()
        
        return {"items": items}