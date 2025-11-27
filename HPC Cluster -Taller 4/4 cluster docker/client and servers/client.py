import itertools
import requests
import concurrent.futures
import time
import json

# Configuration
API_URL = "http://localhost:5000/calculate_distance"
CITIES = [
    {"name": "A", "x": 0, "y": 0},
    {"name": "B", "x": 10, "y": 0},
    {"name": "C", "x": 10, "y": 10},
    {"name": "D", "x": 0, "y": 10},
    {"name": "E", "x": 5, "y": 5}
]

def calculate_route_distance(route):
    """Sends a route to the API and returns the distance."""
    try:
        payload = {"route": route}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("total_distance")
        else:
            print(f"Error: API returned {response.status_code}")
            return float('inf')
    except Exception as e:
        print(f"Request failed: {e}")
        return float('inf')

def main():
    print("Starting TSP Brute Force Client...")
    print(f"Cities: {[c['name'] for c in CITIES]}")
    
    # Generate all permutations of cities
    permutations = list(itertools.permutations(CITIES))
    print(f"Total permutations to check: {len(permutations)}")

    min_distance = float('inf')
    best_route = None
    
    start_time = time.time()

    # Use ThreadPoolExecutor for concurrency
    # This exploits the Swarm load balancing
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Map permutations to futures
        future_to_route = {executor.submit(calculate_route_distance, list(route)): route for route in permutations}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_route)):
            route = future_to_route[future]
            try:
                distance = future.result()
                if distance < min_distance:
                    min_distance = distance
                    best_route = route
                    print(f"New best found: {distance:.2f} -> {[c['name'] for c in route]}")
            except Exception as exc:
                print(f"Route check generated an exception: {exc}")
            
            if i % 10 == 0:
                print(f"Processed {i}/{len(permutations)} routes...", end='\r')

    end_time = time.time()
    
    print("\n" + "="*40)
    print("OPTIMIZATION COMPLETE")
    print("="*40)
    print(f"Best Distance: {min_distance:.2f}")
    if best_route:
        print(f"Best Route: {[c['name'] for c in best_route]}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
