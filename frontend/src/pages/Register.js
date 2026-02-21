import { useState } from "react";
import API from "../api";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const [form, setForm] = useState({ email: "", password: "", role: "user" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async () => {
    try {
      await API.post("/auth/register", form);
      navigate("/login");
    } catch (err) {
      setError("Registration failed. Email may already exist.");
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.box}>
        <h2>🏥 Register</h2>
        {error && <p style={{color:"red"}}>{error}</p>}
        <input style={styles.input} placeholder="Email" onChange={e => setForm({...form, email: e.target.value})} />
        <input style={styles.input} placeholder="Password" type="password" onChange={e => setForm({...form, password: e.target.value})} />
        <select style={styles.input} onChange={e => setForm({...form, role: e.target.value})}>
          <option value="user">User</option>
          <option value="doctor">Doctor</option>
          <option value="admin">Admin</option>
        </select>
        <button style={styles.btn} onClick={handleSubmit}>Register</button>
        <p>Have account? <Link to="/login">Login</Link></p>
      </div>
    </div>
  );
}

const styles = {
  container: { display:"flex", justifyContent:"center", alignItems:"center", height:"100vh", background:"#f0f4f8" },
  box: { background:"white", padding:"40px", borderRadius:"10px", width:"350px", boxShadow:"0 4px 20px rgba(0,0,0,0.1)", display:"flex", flexDirection:"column", gap:"15px" },
  input: { padding:"12px", borderRadius:"5px", border:"1px solid #ddd", fontSize:"16px" },
  btn: { padding:"12px", background:"#1a73e8", color:"white", border:"none", borderRadius:"5px", fontSize:"16px", cursor:"pointer" }
};

export default Register;