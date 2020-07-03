import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name': row[0], 'price': row[1]}}

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
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()  # parser is a class variable
        item = {"name": name, "price": data["price"]}
        # items.append(item)
        try:
            Item.insert(item)
        except:
            return {'message': 'An error occurred while inserting the record'}, 500 # Internal server error
        

        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'],item['price']))

        connection.commit()
        connection.close()


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
        data = parser.parse_args()  # parser is a class variable
        # item = next(filter(lambda x: x["name"] == name, items), None)
        # if item is None:
        #     item = {"name": name, "price": data["price"]}
        #     items.append(item)
        # else:
        #     item.update(data)
        item = Item.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message': 'An error occurred while inserting the item'}, 500 # Internal server error
            
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message': 'An error occurred while updating the item'}, 500 # Internal server error
            

        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (item['price'],item['name']))

        connection.commit()
        connection.close()


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