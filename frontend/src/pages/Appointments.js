import { useEffect, useState } from "react";
import API from "../api";

function Appointments() {
  const [appointments, setAppointments] = useState([]);
  const [form, setForm] = useState({ patient_id:"", doctor_id:"", date:"", time:"", reason:"", status:"scheduled" });

  useEffect(() => { API.get("/appointments/").then(res => setAppointments(res.data)); }, []);

  const addAppointment = async () => {
    await API.post("/appointments/", {...form, patient_id: parseInt(form.patient_id), doctor_id: parseInt(form.doctor_id)});
    const res = await API.get("/appointments/");
    setAppointments(res.data);
  };

  return (
    <div style={styles.container}>
      <h2>📅 Appointments</h2>
      <div style={styles.form}>
        <input style={styles.input} placeholder="Patient ID" onChange={e => setForm({...form, patient_id: e.target.value})} />
        <input style={styles.input} placeholder="Doctor ID" onChange={e => setForm({...form, doctor_id: e.target.value})} />
        <input style={styles.input} type="date" onChange={e => setForm({...form, date: e.target.value})} />
        <input style={styles.input} type="time" onChange={e => setForm({...form, time: e.target.value})} />
        <input style={styles.input} placeholder="Reason" onChange={e => setForm({...form, reason: e.target.value})} />
        <button style={styles.btn} onClick={addAppointment}>Book Appointment</button>
      </div>
      <table style={styles.table}>
        <thead>
          <tr><th>ID</th><th>Patient ID</th><th>Doctor ID</th><th>Date</th><th>Time</th><th>Reason</th><th>Status</th></tr>
        </thead>
        <tbody>
          {appointments.map(a => (
            <tr key={a.id}>
              <td>{a.id}</td>
              <td>{a.patient_id}</td>
              <td>{a.doctor_id}</td>
              <td>{a.date}</td>
              <td>{a.time}</td>
              <td>{a.reason}</td>
              <td>{a.status}</td>
            </tr>
          ))}
        </tbody>
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

export default Appointments;
