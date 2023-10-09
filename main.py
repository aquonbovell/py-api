from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://aquon123:bovell123@api.k89yiaj.mongodb.net/?retryWrites=true&w=majority"

# Create a new MongoDB client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['users']
users = db['users']

# Send a ping to confirm a successful connection
try:
  client.admin.command('ping')
  print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
  print(e)

# Create a Flask app
app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
	try:
		data = list(users.find({}))
		users_list = [{"_id": str(user["_id"]), "username": user['username'], "age": user['age']} for user in data]
		return jsonify(users_list), 200
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['POST'])
def create_user():
	try:
		data = request.get_json()
		if "username" not in data or "age" not in data:
			return jsonify({"error": "Both 'username' and 'age' are required fields."}), 400

		user_id = users.insert_one(data).inserted_id
		return jsonify({"_id": str(user_id), "username": data['username'], "age": data['age']}), 201
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route('/users/<user_name>', methods=['PUT'])
def update_user(user_name):
	try:
		data = request.get_json()
		result = users.update_one({"username": user_name}, {"$set": data})
		if result.matched_count == 0:
			return jsonify({"error": "User not found."}), 404
		return jsonify({}), 204
	except Exception as e:
		return jsonify({"error": str(e)}), 500

@app.route('/users/<user_name>', methods=['DELETE'])
def delete_user(user_name):
	try:
		result = users.delete_one({"username": user_name})
		if result.deleted_count == 0:
			return jsonify({"error": "User not found."}), 404
		return jsonify({}), 204
	except Exception as e:
		return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
	app.run(debug=True)
