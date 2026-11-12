import { Routes, Route, Link, Navigate } from "react-router-dom";
import Login from "./screens/Login";
import RestaurantList from "./screens/customer/RestaurantList";
import Menu from "./screens/customer/Menu";
import OrderStatus from "./screens/customer/OrderStatus";
import Dashboard from "./screens/restaurant/Dashboard";
import MenuManagement from "./screens/restaurant/MenuManagement";

export default function App() {
  return (
    <>
      <nav>
        <Link to="/customer">Customer</Link> |{" "}
        <Link to="/restaurant">Restaurant</Link> |{" "}
        <Link to="/login">Login</Link>
      </nav>

      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/customer" element={<RestaurantList />} />
        <Route path="/customer/restaurant/:id" element={<Menu />} />
        <Route path="/customer/order/:orderId" element={<OrderStatus />} />
        <Route path="/restaurant" element={<Dashboard />} />
        <Route path="/restaurant/menu" element={<MenuManagement />} />
      </Routes>
    </>
  );
}