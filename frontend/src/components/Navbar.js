import { Link, useNavigate } from "react-router-dom";

function Navbar() {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <nav style={styles.nav}>
      <h2 style={styles.logo}>🏥 Hospital AI</h2>
      <div style={styles.links}>
        <Link style={styles.link} to="/">Dashboard</Link>
        <Link style={styles.link} to="/doctors">Doctors</Link>
        <Link style={styles.link} to="/patients">Patients</Link>
        <Link style={styles.link} to="/appointments">Appointments</Link>
        <button style={styles.logout} onClick={logout}>Logout</button>
      </div>
    </nav>
  );
}

const styles = {
  nav: { display:"flex", justifyContent:"space-between", alignItems:"center", background:"#1a73e8", padding:"10px 30px" },
  logo: { color:"white", margin:0 },
  links: { display:"flex", gap:"20px", alignItems:"center" },
  link: { color:"white", textDecoration:"none", fontWeight:"bold" },
  logout: { background:"red", color:"white", border:"none", padding:"8px 16px", borderRadius:"5px", cursor:"pointer" }
};

export default Navbar;