from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# Create a Flask app
app = Flask(__name__)

# Create a MongoDB client using environment variables
MONGO_URI = os.getenv("MONGO_URI")

if MONGO_URI is None:
    raise ValueError("MONGO_URI environment variable is not set. Please set it.")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))

db = client['users']
users = db['users']

@app.route('/users', methods=['GET'])
def get_users():
    try:
        data = users.find({})
        users_list = [{"username": user['username'], "age": user['age']} for user in data]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/createuser', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        users.insert_one(data)
        return jsonify({"username": data['username'], "age": data['age']}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/updateuser/<name>', methods=['PUT'])
def update_user(name):
    try:
        users.update_one({"username": name}, {"$set": request.get_json()})
        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deleteuser/<name>', methods=['DELETE'])
def delete_user(name):
    try:
        users.delete_one({"username": name})
        return jsonify({}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
