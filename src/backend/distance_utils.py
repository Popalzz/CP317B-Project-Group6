import math

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