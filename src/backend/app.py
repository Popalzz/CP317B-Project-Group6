import math
from flask import Flask, jsonify, request

app = Flask(__name__)
#temp restaurants for testing
restaurants = [
        {
                "id": 1,
                "name": "Pizza Palace",
                "latitude": 43.4643,
                "longitude": -80.5204
        },
        {
                "id": 2,
                "name": "Burger Fact",
                "latitude": 43.3681,
                "longitude": -80.4925
        },
        {
                "id": 3,
                "name": "Tim's",
                "latitude": 43.3681,
                "longitude": -80.3187
        }
]

def calculate_dist(lat1, lon1, lat2, lon2):
	earth_rad = 6371
	
	#convert deg to rad
	lat1 = math.radians(lat1)
	lon1 = math.radians(lon1)
	lat2 = math.radians(lat2)
	lon2 = math.radians(lon2)

	#calc difference
	delta_lat = lat2 - lat1
	delta_lon = lon2 - lon1

	#haversine formula
	a = (
		math.sin(delta_lat / 2) ** 2
		+ math.cos(lat1) * math.cos(lat2)
		* math.sin(delta_lon / 2) ** 2
	)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	return earth_rad * c


# Home endpoint
@app.route("/")
def home():
	return jsonify({
		"message": "Food Delivery System API is running"
	})

#Restaurant browse endpoint
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
	customer_lat = request.args.get("lat", type=float)
	customer_lon = request.args.get("lon", type=float)
	
	if customer_lat is None or customer_lon is None:
		return jsonify({"error": "Missing or invalid coordinates"}), 400
	
	if customer_lat < -90 or customer_lat > 90:
		return jsonify({"error": "Coordinates out of range"}), 400

	if customer_lon < -180 or customer_lon > 180:
		return jsonify({"error": "Coordinates out of range"}), 400

	if math.isfinite(customer_lat) is not True or math.isfinite(customer_lon) is not True:
		return jsonify({"error": "Invalid coordinates"}), 400

	eligible_rest = []
		
	for restaurant in restaurants:
		rest_lat = restaurant["latitude"]
		rest_lon = restaurant["longitude"]
		
		distance = calculate_dist(customer_lat, customer_lon, rest_lat, rest_lon)
		
		if distance <= 35:
			eligible_rest.append(restaurant)
			
		
	return jsonify(eligible_rest)

print("test distance", calculate_dist(43.45, -80.49, 43.45, -80.49))
if __name__ == "__main__":
	app.run(debug=True, port=5000)



