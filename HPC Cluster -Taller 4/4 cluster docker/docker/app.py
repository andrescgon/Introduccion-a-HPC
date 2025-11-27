from flask import Flask, request, jsonify
import math

app = Flask(__name__)

def calculate_euclidean_distance(p1, p2):
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2)

@app.route('/calculate_distance', methods=['POST'])
def calculate_distance():
    """
    Calculates the total distance of a route.
    
    JSON Input:
    {
        "route": [
            {"name": "A", "x": 0, "y": 0},
            {"name": "B", "x": 3, "y": 4},
            ...
        ]
    }
    """
    data = request.get_json()
    route = data.get('route', [])
    
    if not route or len(route) < 2:
        return jsonify({"total_distance": 0, "message": "At least two cities are required"}), 200

    # Calculate total distance for the sequence of cities
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_euclidean_distance(route[i], route[i+1])
    
    return jsonify({
        "total_distance": total_distance
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



