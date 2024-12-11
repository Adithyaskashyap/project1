from flask import request, jsonify
from flask import Flask,Blueprint
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash

authenticate_route=Blueprint('authenticate',__name__)
client = MongoClient('mongodb://localhost:27017/') 
db = client['Travel']
users_collection = db['users']


@authenticate_route.route('/register', methods=['POST','GET'])
def register():
    #return "Hello people"
    data = request.get_json()
    username = data.get('username')
    usermail= data.get('usermail')
    password = data.get('password')
    confirm_password=data.get('confirm_password')
    if password!=confirm_password:
        return jsonify({'message':'Passwords does not match'})
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'User already exists'}), 400

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({'username': username,'usermail':usermail,'password': hashed_pw})
    return jsonify({'message': 'User registered successfully'}), 201
@authenticate_route.route('/login',methods=['POST','GET'])
def login():
    #return "Hello everyone"
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid username or password'}), 401
if __name__=="__main__":
    app.run(debug=True)