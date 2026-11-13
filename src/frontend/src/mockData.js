export const restaurants = [
    { id: 1, name: "Pizza Palace", cuisine: "Italian", distanceKm: 4.2 },
    { id: 2, name: "Sushi House", cuisine: "Japanese", distanceKm: 12.8 },
    { id: 3, name: "Burger Barn", cuisine: "American", distanceKm: 27.5 },
    { id: 4, name: "Far Away Diner", cuisine: "Diner", distanceKm: 48.0 },
  ];
  
  // placeholder API call. Swap for real call to Amir's backend later.
  export function fetchRestaurants(location) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(restaurants.filter((r) => r.distanceKm <= 35));
      }, 800);
    });
  }