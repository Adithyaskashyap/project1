import math
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the geodesic distance between two coordinates."""
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers

def total_distance_tsp(route, coordinates):
    """Calculate the total distance of a TSP route."""
    distance = 0
    for i in range(len(route)):
        city1 = coordinates[route[i]]
        city2 = coordinates[route[(i + 1) % len(route)]]  # Wrap back to the start
        distance += calculate_distance(city1["lat"], city1["lon"], city2["lat"], city2["lon"])
    return distance

def simulated_annealing_tsp(cities, coordinates, initial_temp=10000, cooling_rate=0.995, max_iter=1000):
    """Simulated Annealing to solve TSP."""
    current_solution = cities[:]
    current_distance = total_distance_tsp(current_solution, coordinates)
    best_solution = current_solution[:]
    best_distance = current_distance
    temp = initial_temp

    for iteration in range(max_iter):
        # Generate a neighbor by swapping two cities
        new_solution = current_solution[:]
        i, j = random.sample(range(1, len(cities)), 2)  # Exclude the first city (source)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

        # Calculate the distance for the new route
        new_distance = total_distance_tsp(new_solution, coordinates)

        # Decide whether to accept the new solution
        if new_distance < current_distance or random.random() < math.exp((current_distance - new_distance) / temp):
            current_solution = new_solution
            current_distance = new_distance

        # Update the best solution found
        if current_distance < best_distance:
            best_solution = current_solution
            best_distance = current_distance

        # Cool down the temperature
        temp *= cooling_rate

    return best_solution, best_distance

def get_coordinates_tsp(cities):
    """Fetch latitude and longitude for a list of cities."""
    geolocator = Nominatim(user_agent="tsp_solver")
    coordinates = {}
    for city in cities:
        location = geolocator.geocode(city)
        if location:
            coordinates[city] = {"lat": location.latitude, "lon": location.longitude}
        else:
            raise ValueError(f"Could not fetch coordinates for city: {city}")
    return coordinates
