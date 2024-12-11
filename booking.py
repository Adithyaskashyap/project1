from flask import Flask, request, jsonify,Blueprint
from pymongo import MongoClient
package_route = Blueprint('package',__name__)


client = MongoClient('mongodb://localhost:27017/') 
db = client['Travel']
users_collection = db['bookings']
@package_route.route('/package_booking', methods=['POST','GET'])
def package_booking():
    #return "hello"
  
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    destination = data.get('destination')
    special_requests = data.get('special_requests', '')

   
    if not email or not name or not destination:
        return jsonify({"message": "Name, email, and destination are required!"}), 400

   
    user = db.users.find_one({"usermail":email })
    if not user:
        return jsonify({"message": "Email not registered! Please register first."}), 403

  
    booking = {
        "name": name,
        "email": email,
        "destination": destination,
        "special_requests": special_requests
    }
    db.booking.insert_one(booking)

    return jsonify({"message": "Package booked successfully!"}), 200

