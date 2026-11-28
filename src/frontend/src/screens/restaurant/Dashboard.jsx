import { useEffect, useState } from "react";
import {
  fetchRestaurantOrders,
  updateOrderStatus,
} from "../../api";

const REFRESH_MS = 3000;

export default function Dashboard() {
  const restaurantId = 1;

  const [orders, setOrders] = useState([]);
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Load once, then refresh every few seconds so new orders show up
  // without a manual reload.
  useEffect(() => {
    let cancelled = false;

    async function refresh() {
      try {
        const data = await fetchRestaurantOrders(restaurantId);
        if (cancelled) return;
        setRestaurant(data.restaurant);
        setOrders(data.orders);
        setError("");
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load orders.");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    refresh();
    const timer = setInterval(refresh, REFRESH_MS);

    return () => {
      cancelled = true;
      clearInterval(timer);
    };
  }, []);

  function getNextStatus(status) {
    if (status === "Pending") return "Accepted";
    if (status === "Accepted") return "Preparing";
    if (status === "Preparing") return "Ready";

    return null;
  }

  async function handleStatusUpdate(order) {
    const nextStatus = getNextStatus(order.status);

    if (!nextStatus) {
      return;
    }

    try {
      const updatedOrder = await updateOrderStatus(
        order.order_id,
        nextStatus
      );

      setError("");
      setOrders((currentOrders) =>
        currentOrders.map((currentOrder) =>
          currentOrder.order_id === updatedOrder.order_id
            ? updatedOrder
            : currentOrder
        )
      );
    } catch (err) {
      setError(err.message || "Failed to update order.");
    }
  }

  if (loading) {
    return <p>Loading restaurant orders...</p>;
  }

  return (
    <main style={{ maxWidth: 700, margin: "0 auto", padding: 16 }}>
      <h1>{restaurant?.name || "Restaurant"} Dashboard</h1>

      {/* Shown above the orders instead of replacing the page, so a brief
          network error during a refresh doesn't hide the order list. */}
      {error && <p role="alert">{error}</p>}

      {orders.length === 0 ? (
        <p>No orders yet.</p>
      ) : (
        orders.map((order) => {
          const nextStatus = getNextStatus(order.status);

          return (
            <div
              key={order.order_id}
              style={{
                border: "1px solid #ccc",
                padding: 16,
                marginBottom: 16,
              }}
            >
              <h2>Order #{order.order_id}</h2>

              <p>
                <strong>Status:</strong> {order.status}
              </p>

              <p>
                <strong>Total:</strong> ${order.total.toFixed(2)}
              </p>

              <h3>Items</h3>

              <ul>
                {order.items.map((item) => (
                  <li key={item.item_id}>
                    Item #{item.item_id} × {item.quantity}
                  </li>
                ))}
              </ul>

              {nextStatus && (
                <button onClick={() => handleStatusUpdate(order)}>
                  Move to {nextStatus}
                </button>
              )}

              {!nextStatus && (
                <p>Restaurant processing complete.</p>
              )}
            </div>
          );
        })
      )}
    </main>
  );
}