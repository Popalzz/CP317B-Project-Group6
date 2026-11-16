import { useState } from "react";
import { Link } from "react-router-dom";
import { fetchRestaurants, LOCATIONS } from "../../api";

export default function RestaurantList() {
  const [locationIndex, setLocationIndex] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [error, setError] = useState("");

  async function handleSearch(e) {
    e.preventDefault();
    if (locationIndex === "") {
      setError("Please choose a delivery location.");
      return;
    }
    const { lat, lon } = LOCATIONS[locationIndex];
    setError("");
    setLoading(true);
    setSearched(true);
    try {
      setResults(await fetchRestaurants(lat, lon));
    } catch (err) {
      setResults([]);
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 600, margin: "0 auto", padding: 16 }}>
      <h1>Find Restaurants</h1>

      <form onSubmit={handleSearch}>
        <label htmlFor="location">Delivery Location</label>
        <br />
        <select
          id="location"
          value={locationIndex}
          onChange={(e) => setLocationIndex(e.target.value)}
          style={{ width: "70%", padding: 8, fontSize: 16 }}
        >
          <option value="">Choose a location</option>
          {LOCATIONS.map((l, i) => (
            <option key={l.label} value={i}>{l.label}</option>
          ))}
        </select>
        <button type="submit" style={{ padding: 8, fontSize: 16, marginLeft: 8 }}>
          Search
        </button>
      </form>

      {error && <p role="alert">{error}</p>}
      {loading && <p>Searching for restaurants within 35 km...</p>}

      {!loading && searched && results.length === 0 && !error && (
        <p>No restaurants deliver to your location.</p>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {results.map((r) => (
          <li
            key={r.id}
            style={{
              border: "1px solid #888",
              borderRadius: 8,
              padding: 12,
              marginTop: 12,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div>
              <strong>{r.name}</strong>
            </div>
            <Link to={`/customer/restaurant/${r.id}`}>View Menu</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}