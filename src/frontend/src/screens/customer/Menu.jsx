import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchMenu } from "../../api";

export default function Menu() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [cart, setCart] = useState({}); // { itemId: quantity }

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError("");
    fetchMenu(id)
      .then((data) => {
        if (cancelled) return;
        setRestaurant(data.restaurant);
        setItems(data.items);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message || "Something went wrong.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  function addItem(itemId) {
    setCart((c) => ({ ...c, [itemId]: (c[itemId] || 0) + 1 }));
  }

  function removeItem(itemId) {
    setCart((c) => {
      const qty = (c[itemId] || 0) - 1;
      const next = { ...c };
      if (qty <= 0) delete next[itemId];
      else next[itemId] = qty;
      return next;
    });
  }

  const cartItems = items.filter((i) => cart[i.id]);
  const total = cartItems.reduce((sum, i) => sum + i.price * cart[i.id], 0);

  return (
    <main style={{ maxWidth: 600, margin: "0 auto", padding: 16 }}>
      <Link to="/customer">← Back to restaurants</Link>

      {loading && <p>Loading menu...</p>}
      {error && <p role="alert">{error}</p>}

      {restaurant && <h1>{restaurant.name}</h1>}

      {!loading && !error && items.length === 0 && (
        <p>This restaurant has no menu items yet.</p>
      )}

      <ul style={{ listStyle: "none", padding: 0 }}>
        {items.map((item) => (
          <li
            key={item.id}
            style={{
              border: "1px solid #888",
              borderRadius: 8,
              padding: 12,
              marginTop: 12,
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              gap: 12,
            }}
          >
            <div>
              <strong>{item.name}</strong>
              <div>{item.description}</div>
              <div>${item.price.toFixed(2)}</div>
            </div>
            <div style={{ whiteSpace: "nowrap" }}>
              <button
                onClick={() => removeItem(item.id)}
                disabled={!cart[item.id]}
                aria-label={`Remove one ${item.name}`}
                style={{ padding: "6px 12px", fontSize: 16 }}
              >
                −
              </button>
              <span style={{ margin: "0 10px" }}>{cart[item.id] || 0}</span>
              <button
                onClick={() => addItem(item.id)}
                aria-label={`Add one ${item.name}`}
                style={{ padding: "6px 12px", fontSize: 16 }}
              >
                +
              </button>
            </div>
          </li>
        ))}
      </ul>

      {cartItems.length > 0 && (
        <section style={{ marginTop: 24 }}>
          <h2>Your Order</h2>
          <ul>
            {cartItems.map((i) => (
              <li key={i.id}>
                {cart[i.id]} × {i.name} — ${(i.price * cart[i.id]).toFixed(2)}
              </li>
            ))}
          </ul>
          <p>
            <strong>Total: ${total.toFixed(2)}</strong>
          </p>
          <button style={{ padding: 10, fontSize: 16 }} disabled>
            Place Order (coming next)
          </button>
        </section>
      )}
    </main>
  );
}