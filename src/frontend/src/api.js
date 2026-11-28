export const LOCATIONS = [
    { label: "Waterloo", lat: 43.4643, lon: -80.5204 },
    { label: "Kitchener", lat: 43.4516, lon: -80.4925 },
    { label: "Toronto (out of range)", lat: 43.6532, lon: -79.3832 },
  ];
  
  export async function fetchRestaurants(lat, lon) {
    const res = await fetch(`/api/restaurants?lat=${lat}&lon=${lon}`);
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Request failed");
    return data;
  }

// Temporary menus, keyed by the restaurant ids in Amir's app.py.
// Replace fetchMenu with a real fetch once a menu endpoint exists.
const MENUS = {
    1: {
      restaurant: { id: 1, name: "Pizza Palace" },
      items: [
        { id: 101, name: "Margherita Pizza", description: "Tomato, mozzarella, basil", price: 14.99 },
        { id: 102, name: "Pepperoni Pizza", description: "Pepperoni and mozzarella", price: 16.99 },
        { id: 103, name: "Garlic Bread", description: "Toasted with garlic butter", price: 6.5 },
      ],
    },
    2: {
      restaurant: { id: 2, name: "Burger Fact" },
      items: [
        { id: 201, name: "Classic Burger", description: "Beef patty, lettuce, tomato", price: 12.99 },
        { id: 202, name: "Cheese Fries", description: "Fries with melted cheese", price: 7.25 },
        { id: 203, name: "Milkshake", description: "Vanilla, chocolate or strawberry", price: 5.99 },
      ],
    },
    3: {
      restaurant: { id: 3, name: "Tim's" },
      items: [
        { id: 301, name: "Coffee", description: "Freshly brewed", price: 2.25 },
        { id: 302, name: "Breakfast Sandwich", description: "Egg, cheese and bacon", price: 5.49 },
        { id: 303, name: "Donut", description: "Assorted flavours", price: 1.79 },
      ],
    },
  };
  
  export async function fetchMenu(restaurantId) {
    const res = await fetch(`/api/restaurants/${restaurantId}/menu`);
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Failed to load menu");
    }

    return data;
  }

  export async function createOrder(orderData) {
    const res = await fetch("/api/orders", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(orderData),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Failed to place order");
    }

    return data;
  }

  export async function fetchOrder(orderId) {
    const res = await fetch(`/api/orders/${orderId}`);
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Failed to load order");
    }

    return data;
  }

  export async function fetchRestaurantOrders(restaurantId) {
  const res = await fetch(`/api/restaurants/${restaurantId}/orders`);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to load restaurant orders");
  }

  return data;
}

export async function updateOrderStatus(orderId, status) {
  const res = await fetch(`/api/orders/${orderId}/status`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ status }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to update order status");
  }

  return data;
}

export async function fetchAvailableDeliveries() {
  const res = await fetch("/api/deliveries/available");
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to load deliveries");
  }

  return data;
}

export async function acceptDelivery(orderId, driverId) {
  const res = await fetch(`/api/orders/${orderId}/accept-delivery`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ driver_id: driverId }),
  });

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to accept delivery");
  }

  return data;
}

export async function fetchOrderEta(orderId) {
  const res = await fetch(`/api/orders/${orderId}/eta`);
  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.error || "Failed to load delivery estimate");
  }

  return data;
}