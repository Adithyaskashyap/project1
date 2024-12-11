from flask import Blueprint, request, jsonify
from a_simul import simulated_annealing_tsp, get_coordinates_tsp
from pymongo import MongoClient

tsp_routes = Blueprint("tsp", __name__)
client = MongoClient("mongodb://localhost:27017/")  
db = client["Travel"]  
collection = db["tourist_places"]

@tsp_routes.route("/solve_tsp", methods=["POST", "GET"])
def solve_tsp():
    try:
        # Parse JSON input
        data = request.get_json()
        source_city = data.get("source_city")
        num_cities = data.get("num_cities") 
        cities = data.get("cities", [])
        
        initial_temp = 10000
        cooling_rate = 0.995
        max_iter = 1000

        if not source_city or not cities or not num_cities:
            return jsonify({"error": "Source city, cities list, and number of cities are required"}), 400

        
        if source_city in cities:
            return jsonify({"error": "Source city should not be included in the cities list"}), 400

        
        if len(cities) != num_cities:
            return jsonify({"error": "Number of cities does not match the length of the cities list"}), 400

       
        invalid_cities = []
        for destination in cities:
            db_result = collection.find_one({"name": {"$regex": f"^{destination}$", "$options": "i"}})
            if not db_result:
                invalid_cities.append(destination)

       
        if invalid_cities:
            return jsonify({"error": f"The following cities were not found in the database: {', '.join(invalid_cities)}"}), 404

        cities = [source_city] + cities
        coordinates = get_coordinates_tsp(cities) 

        
        optimal_path, optimal_distance = simulated_annealing_tsp(cities, coordinates, initial_temp, cooling_rate, max_iter)
        city_details = []
        for city in best_route:
            city_info = city_collection.find_one({"name": city}, {"_id": 0})  # Find city details and exclude _id
            if city_info:
            city_details.append(city_info)
        return jsonify({
            "optimal_path": optimal_path,
            "optimal_distance": f"{optimal_distance:.2f} km",
            "city_details": city_details
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
