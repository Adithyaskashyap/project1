from flask import Blueprint, request, jsonify
from a_simul import simulated_annealing_tsp,get_coordinates_tsp

tsp_routes = Blueprint("tsp", __name__)

@tsp_routes.route("/solve_tsp", methods=["POST","GET"])
def solve_tsp():
    try:
        #return "Hello people"
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


        cities = [source_city] + cities 
        coordinates = get_coordinates_tsp(cities) 


        optimal_path, optimal_distance = simulated_annealing_tsp(cities, coordinates, initial_temp, cooling_rate, max_iter)

        return jsonify({
            "optimal_path": optimal_path,
            "optimal_distance": f"{optimal_distance:.2f} km"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
