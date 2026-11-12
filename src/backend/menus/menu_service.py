"""MENU-1 / MENU-2 menu service scaffold.

Amir with Ervin consuming the API from frontend.

"""
menus = {
    1: {
        1: {
            "name": "Cheese Pizza",
            "price": 14.99,
            "available": True
        },
        2: {
            "name": "Pepperoni Pizza",
            "price": 16.99,
            "available": True
        }
    },
    2: {
        1: {
            "name": "Burger",
            "price": 11.99,
            "available": True
        }
    }
}

def get_menu(restaurant_id: int):
    """Return the current menu for one restaurant.

    Expected result: a list of dictionaries containing at minimum:
    id, name, price, available.

    TODO:
    - Validate restaurant_id.
    - Load menu items from your chosen data/database layer.
    - Return only items belonging to this restaurant.
    - Decide whether unavailable items are returned with available=False or hidden.
    """

    if restaurant_id is None:
        return None

    menu = menus.get(restaurant_id)

    if menu is None:
        return None

    return menu
            
        
    


def add_menu_item(restaurant_id: int, name: str, price: float, available: bool = True):
    """Create a new menu item for a restaurant.

    TODO:
    - Validate non-empty name.
    - Validate price >= 0.
    - Store item and generate an ID.
    - Return the created item.
    """
    rest_menu = get_menu(restaurant_id)
    new_item_id = 0
    if rest_menu is None:
        menus[restaurant_id] = {}
        rest_menu = menus[restaurant_id]

    if not name:
        return None

    if price < 0:
        return None

    if not rest_menu:
        new_item_id = 1
    else:
        new_item_id = max(rest_menu) + 1

    rest_menu[new_item_id] = {
        "name": name,
        "price": price,
        "available": available
    }
    return new_item_id, rest_menu[new_item_id]

    
    


def update_menu_item(restaurant_id: int, item_id: int, updates: dict):
    """Update allowed fields for a restaurant menu item.

    TODO:
    - Confirm the item belongs to restaurant_id.
    - Validate changed price/name/availability.
    - Persist and return the updated item.
    """
    rest_menu = get_menu(restaurant_id)

    if rest_menu is None:
        return None

    if not isinstance(item_id, int) or item_id < 1:
        return None 

    item = rest_menu.get(item_id)
    if not item:
        return None

    if "name" in updates:
        if updates["name"] is None or updates["name"] == "":
            return None
        item["name"] = updates["name"]

    if "price" in updates:
        if updates["price"] is None or updates["price"] == "":
            return None
        item["price"] = updates["price"]

    if "available" in updates:
        if updates["available"] is None:
            return None
        item["available"] = updates["available"]

    return item



def remove_menu_item(restaurant_id: int, item_id: int):
    """Remove or deactivate a menu item.

    TODO:
    - Prefer soft-delete/deactivation if needed so past orders retain item details.
    - Return True on success or a clear not-found result.
    """
    rest_menu = get_menu(restaurant_id)

    if rest_menu is None:
        return None

    if not isinstance(item_id, int) or item_id < 1:
        return None 

    item = rest_menu.get(item_id)
    if not item:
        return None

    item["available"] = False

    return item
