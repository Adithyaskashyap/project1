from flask import Blueprint,request,jsonify
from a_star import a_star_tsp
from pymongo import MongoClient

astar_routes=Blueprint('a_star',__name__)
client = MongoClient("mongodb://localhost:27017/")  
db = client["Travel"]  
collection = db["tourist_places"]


@astar_routes.route('/a_algo',methods=['POST','GET'])
def a_algo():
    #return "HEllo World"
    try:
        data=request.get_json()
        
        source=data.get('source_city')
        num_cities = data.get('num_cities')
        cities=data.get('cities',[])
        if num_cities<=0:
            return jsonify({"error":"Invalid number of cities "}),400
        if source not in cities:
            return jsonify({"error":"Source not in the given city list"}),400
        invalid_cities = []
        for destination in cities:
            db_result = collection.find_one({"name": {"$regex": f"^{destination}$", "$options": "i"}})
            if not db_result:
                invalid_cities.append(destination)

       
        if invalid_cities:
            return jsonify({"error": f"The following cities were not found in the database: {', '.join(invalid_cities)}"}), 404
        optimal_path,min_cost=a_star_tsp(cities, source)
        return jsonify({
        "optimal_path": optimal_path,
        "minimum_cost": f"{min_cost:.2f} km"
        })
    except ValueError as e:
        return jsonify({"error": str(e)}),400
    except Exception as e:
        return jsonify({"error details": str(e)}),500

