import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchOrder, fetchMenu, fetchOrderEta } from "../../api";

const REFRESH_MS = 4000;

// Must match ALLOWED_STATUSES in status_service.py exactly.
const STAGES = [
  "Pending",
  "Accepted",
  "Preparing",
  "Ready",
  "On the way",
  "Delivered",
];

export default function OrderStatus() {
  const { orderId } = useParams();

  const [order, setOrder] = useState(null);
  const [menu, setMenu] = useState(null);
  const [eta, setEta] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    let intervalId;

    async function loadOrder() {
      try {
        const data = await fetchOrder(orderId);

        if (active) {
          setOrder(data);
          setError("");
        }

        // Nothing changes after delivery, so stop polling.
        if (data.status === "Delivered") {
          clearInterval(intervalId);
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

    // Refresh every few seconds
    intervalId = setInterval(loadOrder, REFRESH_MS);

    // Stop polling when the user leaves the page
    return () => {
      active = false;
      clearInterval(intervalId);
    };
  }, [orderId]);

  // Look up restaurant and item names once the order is known.
  const restaurantId = order?.restaurant_id;

  useEffect(() => {
    if (restaurantId == null) return;
    let active = true;

    fetchMenu(restaurantId)
      .then((data) => {
        if (active) setMenu(data);
      })
      .catch(() => {
        // Names are a nice-to-have; fall back to ids.
      });

    return () => {
      active = false;
    };
  }, [restaurantId]);

  // The estimate is based on restaurant-to-customer distance and doesn't
  // change as the order moves along, so one fetch per order is enough.
  useEffect(() => {
    let active = true;
    setEta(null);

    fetchOrderEta(orderId)
      .then((data) => {
        if (active) setEta(data);
      })
      .catch(() => {
        // The estimate is optional; the status page works without it.
      });

    return () => {
      active = false;
    };
  }, [orderId]);

  if (loading) {
    return <p>Loading order...</p>;
  }

  // Only a full-page error when there is nothing to show yet.
  if (!order && error) {
    return <p role="alert">{error}</p>;
  }

  if (!order) {
    return <p>Order not found.</p>;
  }

  const currentIndex = STAGES.indexOf(order.status);
  const delivered = order.status === "Delivered";

  function itemLabel(item) {
    const menuItem = menu?.items?.find((i) => i.id === item.item_id);
    return `${menuItem?.name || `Item #${item.item_id}`} × ${item.quantity}`;
  }

  return (
    <main style={{ maxWidth: 600, margin: "0 auto", padding: 16 }}>
      <Link to="/customer">← Back to restaurants</Link>

      <h1>Order #{order.order_id}</h1>

      {/* A refresh failed, but the last known status is still shown. */}
      {error && (
        <p role="alert">
          Connection problem. Showing the last known status and retrying...
        </p>
      )}

      <p>
        <strong>Status:</strong> {order.status}
      </p>

      {delivered ? (
        <p>Your order has been delivered. Enjoy your meal!</p>
      ) : (
        order.delivery_status === "Assigned" && (
          <p>A driver has been assigned to your order.</p>
        )
      )}

      {!delivered && eta && (
        <p>
          <strong>Estimated delivery time:</strong> about {eta.eta_minutes}{" "}
          minutes ({eta.prep_minutes} min preparing + {eta.travel_minutes} min
          travel)
        </p>
      )}

      {/* Progress uses text markers, not colour alone (accessibility). */}
      <h2>Progress</h2>
      <ol style={{ listStyle: "none", padding: 0 }}>
        {STAGES.map((stage, index) => {
          let marker = "○";
          let note = "";

          if (index < currentIndex || delivered) {
            marker = "✓";
            note = " (done)";
          }
          if (index === currentIndex && !delivered) {
            marker = "→";
            note = " (current)";
          }

          return (
            <li
              key={stage}
              aria-current={index === currentIndex ? "step" : undefined}
              style={{
                padding: "4px 0",
                fontWeight: index === currentIndex ? "bold" : "normal",
              }}
            >
              {marker} {stage}
              {note}
            </li>
          );
        })}
      </ol>

      <p>
        <strong>Restaurant:</strong>{" "}
        {menu?.restaurant?.name || `#${order.restaurant_id}`}
      </p>

      <h2>Items</h2>

      <ul>
        {order.items.map((item) => (
          <li key={item.item_id}>{itemLabel(item)}</li>
        ))}
      </ul>

      <p>
        <strong>Total: ${order.total.toFixed(2)}</strong>
      </p>
    </main>
  );
}