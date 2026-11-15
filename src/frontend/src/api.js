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