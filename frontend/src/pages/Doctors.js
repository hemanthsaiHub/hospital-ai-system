import { useEffect, useState } from "react";
import API from "../api";

function Doctors() {
  const [doctors, setDoctors] = useState([]);
  const [form, setForm] = useState({ name:"", specialization:"", phone:"", email:"" });

  useEffect(() => { API.get("/doctors/").then(res => setDoctors(res.data)); }, []);

  const addDoctor = async () => {
    await API.post("/doctors/", form);
    const res = await API.get("/doctors/");
    setDoctors(res.data);
  };

  return (
    <div style={styles.container}>
      <h2>🩺 Doctors</h2>
      <div style={styles.form}>
        <input style={styles.input} placeholder="Name" onChange={e => setForm({...form, name: e.target.value})} />
        <input style={styles.input} placeholder="Specialization" onChange={e => setForm({...form, specialization: e.target.value})} />
        <input style={styles.input} placeholder="Phone" onChange={e => setForm({...form, phone: e.target.value})} />
        <input style={styles.input} placeholder="Email" onChange={e => setForm({...form, email: e.target.value})} />
        <button style={styles.btn} onClick={addDoctor}>Add Doctor</button>
      </div>
      <table style={styles.table}>
        <thead><tr><th>ID</th><th>Name</th><th>Specialization</th><th>Phone</th><th>Email</th></tr></thead>
        <tbody>{doctors.map(d => <tr key={d.id}><td>{d.id}</td><td>{d.name}</td><td>{d.specialization}</td><td>{d.phone}</td><td>{d.email}</td></tr>)}</tbody>
      </table>
    </div>
  );
}

const styles = {
  container: { padding:"30px" },
  form: { display:"flex", gap:"10px", marginBottom:"20px", flexWrap:"wrap" },
  input: { padding:"10px", borderRadius:"5px", border:"1px solid #ddd", fontSize:"14px" },
  btn: { padding:"10px 20px", background:"#1a73e8", color:"white", border:"none", borderRadius:"5px", cursor:"pointer" },
  table: { width:"100%", borderCollapse:"collapse", background:"white", borderRadius:"10px", overflow:"hidden", boxShadow:"0 2px 10px rgba(0,0,0,0.1)" }
};

export default Doctors;