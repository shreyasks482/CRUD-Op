from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

uri = "mongodb+srv://ksshreyas124:TDg2uFWfTyplfuXZ@cluster0.zsiztei.mongodb.net/?retryWrites=true&w=majority"

app = Flask(__name__)
api = Api(app)

client = MongoClient(uri)
db = client['pydata']
collection = db['users']

class Users(Resource):
    def get(self):
        try:
            users = []
            for data in collection.find():
                user = {
                    'id': data['id'],
                    'name': data['name'],
                    'email': data['email'],
                    'password': data['password']
                }
                users.append(user)
            return jsonify(users)
        except Exception as e:
            return str(e)

    def post(self):
        try:
            if request.headers['Content-Type'] == 'application/json':
                data = request.get_json()
            else:
                data = request.form
            user = {
                'id': data['id'],
                'name': data['name'],
                'email': data['email'],
                'password': data['password']
            }
            result = collection.insert_one(user)
            return f'User created with id: {result.inserted_id} successfully', 201
        except Exception as e:
            return str(e)


class User(Resource):
    def get(self, id):
        user = collection.find_one({'id': id})
        if user:
            return jsonify({
                'id': user['id'],
                'name': user['name'],
                'email': user['email'],
                'password': user['password']
            })
        else:
            return f"No user found with id: {id}", 404


    def put(self, id):
        query = {'id': id}
        data = request.get_json()
        new_user = {
            'name': data['name'],
            'email': data['email'],
            'password': data['password']
        }
        result = collection.update_one(query, {'$set': new_user})
        if result.modified_count > 0:
            return f"User with id: {id} is updated"
        else:
            return f"User id: {id} is not found", 404


    def delete(self, id):
        result = collection.delete_one({'id': id})
        if result.deleted_count > 0:
            return f"User id: {id} deleted"
        else:
            return f"User id: {id} is not found", 404


api.add_resource(Users, '/users')
api.add_resource(User, '/users/<id>')


if __name__ == "__main__":
    app.run(debug=True)
