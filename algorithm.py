from flask import Blueprint,request,jsonify
from a_star import a_star_tsp
astar_routes=Blueprint('a_star',__name__)

@astar_routes.route('/a_algo',methods=['POST','GET'])
def a_algo():
    #return "HEllo World"
    try:
        data=request.get_json()
        num_cities = data.get('num_cities')
        source=data.get('source_city')
        cities=data.get('cities')
        if num_cities<=0:
            return jsonify({"error":"Invalid number of cities"}),400
        if source not in cities:
            return jsonify({"error":"Source not in the given city list"}),400
        optimal_path,min_cost=a_star_tsp(cities, source)
        return jsonify({
        "optimal_path": optimal_path,
        "minimum_cost": f"{min_cost:.2f} km"
        })
    except ValueError as e:
        return jsonify({"error": str(e)}),400
    except Exception as e:
        return jsonify({"error details": str(e)}),500

