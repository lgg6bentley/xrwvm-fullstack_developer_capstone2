import { Routes, Route, Navigate } from "react-router-dom";
import LoginPanel from "./components/Login/Login";
import Register from "./components/Register/Register";
import FleetList from "./components/Dealers/FleetList"; // 🔧 Importing FleetList
import CarCard from "./components/Dealers/CarCard";
import DealerReviews from "./components/Reviews/DealerReviews";

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<Register />} />
      <Route path="/fleet" element={<FleetList />} /> {/* ✅ Added route for fleet */}
      <Route path="/" element={<Navigate to="/register" />} />
      <Route path="/dealer-reviews" element={<DealerReviews />} />
    </Routes>
  );
}

export default App;