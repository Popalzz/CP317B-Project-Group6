import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchOrder } from "../../api";

export default function OrderStatus() {
  const { orderId } = useParams();

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

useEffect(() => {
  let active = true;

  async function loadOrder() {
    try {
      const data = await fetchOrder(orderId);

      if (active) {
        setOrder(data);
        setError("");
      }
    } catch (err) {
      if (active) {
        setError(err.message || "Failed to load order.");
      }
    } finally {
      if (active) {
        setLoading(false);
      }
    }
  }

  setLoading(true);
  setOrder(null);
  setError("");

  // Fetch immediately when the page opens
  loadOrder();

  // Refresh every 4 seconds
  const intervalId = setInterval(loadOrder, 4000);

  // Stop polling when the user leaves the page
  return () => {
    active = false;
    clearInterval(intervalId);
  };
}, [orderId]);

  if (loading) {
    return <p>Loading order...</p>;
  }

  if (error) {
    return <p role="alert">{error}</p>;
  }

  if (!order) {
    return <p>Order not found.</p>;
  }

  return (
    <main style={{ maxWidth: 600, margin: "0 auto", padding: 16 }}>
      <Link to="/customer">← Back to restaurants</Link>

      <h1>Order #{order.order_id}</h1>

      <p>
        <strong>Status:</strong> {order.status}
      </p>

      <p>
        <strong>Restaurant ID:</strong> {order.restaurant_id}
      </p>

      <h2>Items</h2>

      <ul>
        {order.items.map((item) => (
          <li key={item.item_id}>
            Item #{item.item_id} × {item.quantity}
          </li>
        ))}
      </ul>

      <p>
        <strong>Total: ${order.total.toFixed(2)}</strong>
      </p>
    </main>
  );
}