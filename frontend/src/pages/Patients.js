import { useEffect, useState } from "react";
import API from "../api";

function Patients() {
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({ name:"", age:"", gender:"", phone:"", email:"", blood_group:"", address:"" });

  useEffect(() => { API.get("/patients/").then(res => setPatients(res.data)); }, []);

  const addPatient = async () => {
    await API.post("/patients/", {...form, age: parseInt(form.age)});
    const res = await API.get("/patients/");
    setPatients(res.data);
  };

  return (
    <div style={styles.container}>
      <h2>🏥 Patients</h2>
      <div style={styles.form}>
        <input style={styles.input} placeholder="Name" onChange={e => setForm({...form, name: e.target.value})} />
        <input style={styles.input} placeholder="Age" onChange={e => setForm({...form, age: e.target.value})} />
        <input style={styles.input} placeholder="Gender" onChange={e => setForm({...form, gender: e.target.value})} />
        <input style={styles.input} placeholder="Phone" onChange={e => setForm({...form, phone: e.target.value})} />
        <input style={styles.input} placeholder="Email" onChange={e => setForm({...form, email: e.target.value})} />
        <input style={styles.input} placeholder="Blood Group" onChange={e => setForm({...form, blood_group: e.target.value})} />
        <input style={styles.input} placeholder="Address" onChange={e => setForm({...form, address: e.target.value})} />
        <button style={styles.btn} onClick={addPatient}>Add Patient</button>
      </div>
      <table style={styles.table}>
        <thead><tr><th>ID</th><th>Name</th><th>Age</th><th>Gender</th><th>Phone</th><th>Blood Group</th></tr></thead>
        <tbody>{patients.map(p => <tr key={p.id}><td>{p.id}</td><td>{p.name}</td><td>{p.age}</td><td>{p.gender}</td><td>{p.phone}</td><td>{p.blood_group}</td></tr>)}</tbody>
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

export default Patients;