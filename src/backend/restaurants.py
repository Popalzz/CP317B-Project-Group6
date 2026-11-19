
from distance_utils import calculate_dist
restaurants = {
    1: {
        "owner_id": 101,
        "name": "Pizza Palace",
        "latitude": 43.4643,
        "longitude": -80.5204,
        "is_open": True
    },
    2: {
        "owner_id": 102,
        "name": "Burger Fact",
        "latitude": 43.3681,
        "longitude": -80.4925,
        "is_open": True
    }
}

def get_restaurant_by_id(restaurant_id):
    if restaurant_id is None:
        return None
    
    restaurant = restaurants.get(restaurant_id)

    if restaurant is None:
        return None

    return restaurant


def create_restaurant(owner_id, name, latitude, longitude):
    if not restaurants:
        new_id = 1
    else:
        new_id = max(restaurants.keys()) + 1

    new_rest = {
        "owner_id": owner_id,
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "is_open": True
    }

    restaurants[new_id] = new_rest

    return new_rest

def get_restaurants():
   return restaurants

def get_nearby_restaurants(customer_lat, customer_lon):
    nearby_rest = list()

    for restaurant in restaurants.values():
        rest_lat = restaurant["latitude"]
        rest_lon = restaurant["longitude"]
        
        dist = calculate_dist(customer_lat,customer_lon,rest_lat,rest_lon)

        if dist <= 35 and restaurant["is_open"] == True:
            nearby_rest.append(restaurant)
    return nearby_rest

def update_restaurant(restaurant_id, new_name, new_lat, new_lon, new_is_open):
    restaurant = get_restaurant_by_id(restaurant_id)

    if restaurant is None:
        return False

    if new_name is not None:
        restaurant["name"] = new_name

    if new_lat is not None:
            if new_lat > -90 and new_lat < 90:
                return "Not a valid range for Lat"
            else:
                restaurant["latitude"] = new_lat

    if new_lon is not None:
            if new_lon > -180 and new_lon < 180:
                return "Not a valid range for Lon"
            else:
                restaurant["longitude"] = new_lon

    if new_is_open is not None:
            restaurant["is_open"] = new_is_open

    return restaurant

