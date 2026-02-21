import { useEffect, useState } from "react";
import API from "../api";

function Dashboard() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    API.get("/admin/dashboard").then(res => setStats(res.data)).catch(() => {});
  }, []);

  return (
    <div style={styles.container}>
      <h2>📊 Dashboard</h2>
      {stats ? (
        <div style={styles.grid}>
          <div style={styles.card}><h3>👥 Users</h3><p>{stats.total_users}</p></div>
          <div style={styles.card}><h3>🩺 Doctors</h3><p>{stats.total_doctors}</p></div>
          <div style={styles.card}><h3>🏥 Patients</h3><p>{stats.total_patients}</p></div>
          <div style={styles.card}><h3>📅 Appointments</h3><p>{stats.total_appointments}</p></div>
          <div style={styles.card}><h3>✅ Scheduled</h3><p>{stats.appointments_by_status?.scheduled}</p></div>
          <div style={styles.card}><h3>✔️ Completed</h3><p>{stats.appointments_by_status?.completed}</p></div>
          <div style={styles.card}><h3>❌ Cancelled</h3><p>{stats.appointments_by_status?.cancelled}</p></div>
        </div>
      ) : <p>Loading stats... (Admin access required)</p>}
    </div>
  );
}

const styles = {
  container: { padding:"30px" },
  grid: { display:"grid", gridTemplateColumns:"repeat(4, 1fr)", gap:"20px", marginTop:"20px" },
  card: { background:"white", padding:"20px", borderRadius:"10px", boxShadow:"0 2px 10px rgba(0,0,0,0.1)", textAlign:"center" }
};

export default Dashboard;