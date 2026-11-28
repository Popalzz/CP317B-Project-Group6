import { useEffect, useRef, useState } from "react";
import {
  fetchAvailableDeliveries,
  acceptDelivery,
  fetchMenu,
  fetchOrder,
  updateOrderStatus,
} from "../../api";

// There is no driver login yet. The backend only needs a positive integer.
const DRIVER_ID = 1;
const STORAGE_KEY = "driver-accepted-order-ids";
const REFRESH_MS = 5000;

// The backend has no "my deliveries" endpoint, so we remember accepted order
// ids in the browser and re-fetch them with GET /orders/<id> on reload.
function loadAcceptedIds() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return Array.isArray(saved) ? saved : [];
  } catch {
    return [];
  }
}

function saveAcceptedIds(ids) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(ids));
  } catch {
    // Storage unavailable: the driver just loses the list on reload.
  }
}

// Status names must match ALLOWED_STATUSES in status_service.py exactly.
// The restaurant dashboard stops at "Ready"; the driver takes it from there.
function getNextStatus(status) {
  if (status === "Ready") return "On the way";
  if (status === "On the way") return "Delivered";
  return null;
}

// delivery_location uses latitude/longitude (see validate_order).
// No origin is given, so Google Maps starts from the driver's own location.
function directionsUrl(location) {
  if (!location) return null;
  return `https://www.google.com/maps/dir/?api=1&destination=${location.latitude},${location.longitude}`;
}

export default function Driver() {
  const [available, setAvailable] = useState([]);
  const [myOrders, setMyOrders] = useState([]);
  const [menus, setMenus] = useState({});
  const [declinedIds, setDeclinedIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [busyId, setBusyId] = useState(null);

  const requestedMenus = useRef(new Set());

  // Orders only carry restaurant_id and item_id, so look up names through the
  // existing menu endpoint (once per restaurant).
  function loadMenus(orders) {
    orders.forEach((order) => {
      const id = order.restaurant_id;
      if (requestedMenus.current.has(id)) return;
      requestedMenus.current.add(id);

      fetchMenu(id)
        .then((data) => setMenus((current) => ({ ...current, [id]: data })))
        .catch(() => requestedMenus.current.delete(id));
    });
  }

  useEffect(() => {
    let cancelled = false;

    async function refresh() {
      try {
        const data = await fetchAvailableDeliveries();
        if (cancelled) return;
        setAvailable(data.deliveries);
        setError("");
        loadMenus(data.deliveries);
      } catch (err) {
        if (!cancelled) setError(err.message || "Failed to load deliveries.");
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

  useEffect(() => {
    const ids = loadAcceptedIds();

    Promise.all(ids.map((id) => fetchOrder(id).catch(() => null))).then(
      (orders) => {
        const found = orders.filter(Boolean);
        setMyOrders(found);
        loadMenus(found);
      }
    );
  }, []);

  async function handleAccept(order) {
    setBusyId(order.order_id);
    setError("");

    try {
      const updated = await acceptDelivery(order.order_id, DRIVER_ID);

      setMyOrders((current) => [...current, updated]);
      saveAcceptedIds([...loadAcceptedIds(), updated.order_id]);
      setAvailable((current) =>
        current.filter((o) => o.order_id !== updated.order_id)
      );
    } catch (err) {
      // 409 means another driver accepted it first.
      setError(err.message || "Failed to accept delivery.");
    } finally {
      setBusyId(null);
    }
  }

  // The backend has no decline endpoint, so declining only hides the card here.
  function handleDecline(order) {
    setDeclinedIds((current) => [...current, order.order_id]);
  }

  async function handleStatusUpdate(order) {
    const nextStatus = getNextStatus(order.status);
    if (!nextStatus) return;

    setBusyId(order.order_id);
    setError("");

    try {
      const updated = await updateOrderStatus(order.order_id, nextStatus);

      setMyOrders((current) =>
        current.map((o) => (o.order_id === updated.order_id ? updated : o))
      );
    } catch (err) {
      setError(err.message || "Failed to update order.");
    } finally {
      setBusyId(null);
    }
  }

  function restaurantName(order) {
    return (
      order.restaurant_name ||
      menus[order.restaurant_id]?.restaurant?.name ||
      `Restaurant #${order.restaurant_id}`
    );
  }

  function itemLabel(order, item) {
    const menuItem = menus[order.restaurant_id]?.items?.find(
      (i) => i.id === item.item_id
    );
    return `${menuItem?.name || `Item #${item.item_id}`} × ${item.quantity}`;
  }

  const visibleAvailable = available.filter(
    (order) => !declinedIds.includes(order.order_id)
  );

  const cardStyle = {
    border: "1px solid #ccc",
    padding: 16,
    marginBottom: 16,
  };

  if (loading) {
    return <p>Loading deliveries...</p>;
  }

  return (
    <main style={{ maxWidth: 700, margin: "0 auto", padding: 16 }}>
      <h1>Driver Dashboard</h1>

      {error && <p role="alert">{error}</p>}

      <h2>Available deliveries</h2>

      {visibleAvailable.length === 0 ? (
        <p>No deliveries are ready for pickup right now.</p>
      ) : (
        visibleAvailable.map((order) => (
          <div key={order.order_id} style={cardStyle}>
            <h3>Order #{order.order_id}</h3>

            <p>
              <strong>Pickup:</strong> {restaurantName(order)}
            </p>

            {order.delivery_distance_km != null && (
              <p>
                <strong>Distance to customer:</strong>{" "}
                {order.delivery_distance_km} km
              </p>
            )}

            <ul>
              {order.items.map((item) => (
                <li key={item.item_id}>{itemLabel(order, item)}</li>
              ))}
            </ul>

            {/* The customer's address is deliberately not shown until the
                driver accepts (NFR-2, DRV-1 criterion 3). */}
            <button
              onClick={() => handleAccept(order)}
              disabled={busyId === order.order_id}
            >
              Accept
            </button>{" "}
            <button
              onClick={() => handleDecline(order)}
              disabled={busyId === order.order_id}
            >
              Decline
            </button>
          </div>
        ))
      )}

      <h2>My deliveries</h2>

      {myOrders.length === 0 ? (
        <p>You have not accepted any deliveries.</p>
      ) : (
        myOrders.map((order) => {
          const nextStatus = getNextStatus(order.status);
          const url = directionsUrl(order.delivery_location);

          return (
            <div key={order.order_id} style={cardStyle}>
              <h3>Order #{order.order_id}</h3>

              <p>
                <strong>Pickup:</strong> {restaurantName(order)}
              </p>

              <p>
                <strong>Status:</strong> {order.status}
              </p>

              <ul>
                {order.items.map((item) => (
                  <li key={item.item_id}>{itemLabel(order, item)}</li>
                ))}
              </ul>

              {url ? (
                <p>
                  <a href={url} target="_blank" rel="noopener noreferrer">
                    Open directions to customer
                  </a>
                </p>
              ) : (
                <p>Directions are unavailable for this order.</p>
              )}

              {nextStatus ? (
                <button
                  onClick={() => handleStatusUpdate(order)}
                  disabled={busyId === order.order_id}
                >
                  Mark as {nextStatus}
                </button>
              ) : (
                <p>Delivery complete.</p>
              )}
            </div>
          );
        })
      )}
    </main>
  );
}