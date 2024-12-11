from flask import Flask
from algorithm1 import tsp_routes
from algorithm import astar_routes
from booking import package_route
from login import authenticate_route

app = Flask(__name__)
app.register_blueprint(tsp_routes, url_prefix="/api")
app.register_blueprint(astar_routes, url_prefix="/api")
app.register_blueprint(package_route, url_prefix="/api")
app.register_blueprint(authenticate_route, url_prefix="/api")
if __name__ == "__main__":
    app.run(debug=True)
