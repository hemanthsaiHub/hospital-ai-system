import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Doctors from "./pages/Doctors";
import Patients from "./pages/Patients";
import Appointments from "./pages/Appointments";
import Navbar from "./components/Navbar";

function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<PrivateRoute><Navbar /><Dashboard /></PrivateRoute>} />
        <Route path="/doctors" element={<PrivateRoute><Navbar /><Doctors /></PrivateRoute>} />
        <Route path="/patients" element={<PrivateRoute><Navbar /><Patients /></PrivateRoute>} />
        <Route path="/appointments" element={<PrivateRoute><Navbar /><Appointments /></PrivateRoute>} />
      </Routes>
    </Router>
  );
}

export default App;