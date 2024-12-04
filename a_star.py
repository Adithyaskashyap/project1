import math
from queue import PriorityQueue
from geopy.geocoders import Nominatim

def get_coordinates_tsp(cities):
    """
    Fetch latitude and longitude for a list of cities using Nominatim geocoder.
    """
    geolocator = Nominatim(user_agent="tsp_solver")
    coordinates = {}
    for city in cities:
        location = geolocator.geocode(city)
        if location:
            coordinates[city] = {"lat": location.latitude, "lon": location.longitude}
        else:
            raise ValueError(f"Could not fetch coordinates for city: {city}")
    return coordinates

# Haversine distance to calculate straight-line distance between two coordinates
def haversine(coord1, coord2):
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# A* Algorithm for optimal tour
def a_star_tsp(cities, source_city):
    # Get coordinates for each city
    city_coords = get_coordinates_tsp(cities)
    source_coords = (city_coords[source_city]["lat"], city_coords[source_city]["lon"])
    
    # Priority Queue for A* (cost, current path, remaining cities)
    pq = PriorityQueue()
    pq.put((0, [source_city], set(cities) - {source_city}))
    
    optimal_path = []
    min_cost = float('inf')
    
    while not pq.empty():
        cost, path, remaining = pq.get()
        
        # If no cities are left, add return cost to source city and update min_cost
        if not remaining:
            return_cost = haversine((city_coords[path[-1]]["lat"], city_coords[path[-1]]["lon"]), source_coords)
            total_cost = cost + return_cost
            if total_cost < min_cost:
                min_cost = total_cost
                optimal_path = path + [source_city]
            continue
        
        # For each remaining city, calculate new cost and heuristic
        for next_city in remaining:
            next_coords = (city_coords[next_city]["lat"], city_coords[next_city]["lon"])
            last_coords = (city_coords[path[-1]]["lat"], city_coords[path[-1]]["lon"])
            new_cost = cost + haversine(last_coords, next_coords)
            heuristic = haversine(next_coords, source_coords)
            pq.put((new_cost + heuristic, path + [next_city], remaining - {next_city}))
    
    return optimal_path, min_cost

# required only for terminal running
if __name__ == "__main__":
    
    num_cities = int(input("Enter the number of cities: "))
    cities = []
    for _ in range(num_cities):
        city = input("Enter city name: ")
        cities.append(city)

    source_city = input("Enter the source city: ")

    try:
        optimal_path, min_cost = a_star_tsp(cities, source_city)
        print(f"Optimal Path: {' -> '.join(optimal_path)}")
        print(f"Minimum Cost: {min_cost:.2f} km")
    except ValueError as e:
        print(e)
