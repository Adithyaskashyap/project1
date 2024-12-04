from flask import request, jsonify
from flask import Flask
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash,check_password_hash
app=Flask(__name__)
app.config["MONGO_URI"]="mongodb://localhost:27017/Travel"
mongo=PyMongo(app)
@app.route('/register', methods=['POST','GET'])
def register():
    #return "Hello people"
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if mongo.db.users.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password)
    mongo.db.users.insert_one({'username': username, 'password': hashed_pw})
    return jsonify({'message': 'User registered successfully'}), 201
@app.route('/login',methods=['POST'])
def login():
    #return "Hello everyone"
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401
if __name__=="__main__":
    app.run(debug=True)