import { useState, useEffect } from "react"
import axios from "axios"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || "")
  const [incidents, setIncidents] = useState([])
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [msg, setMsg] = useState("")
  const empty = { device_name: "", location: "", incident_type: "", severity: "low", description: "", status: "open" }
  const [form, setForm] = useState(empty)

  useEffect(() => { load() }, [])

  async function load() {
    const res = await axios.get(`${API}/incidents`)
    setIncidents(res.data)
  }

  async function login() {
    try {
      const res = await axios.post(`${API}/token`, new URLSearchParams({ username, password }))
      setToken(res.data.access_token)
      localStorage.setItem("token", res.data.access_token)
      setMsg("Logged in!")
    } catch {
      setMsg("Login failed")
    }
  }

  function logout() {
    setToken("")
    localStorage.removeItem("token")
    setMsg("")
  }

  async function create() {
    try {
      await axios.post(`${API}/incidents`, form, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setForm(empty)
      setMsg("Incident created!")
      load()
    } catch {
      setMsg("Failed - are you logged in?")
    }
  }

  async function remove(id) {
    await axios.delete(`${API}/incidents/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    load()
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>Network Incident Reporter</h1>

      {!token ? (
        <div>
          <h2>Login</h2>
          <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
          {" "}
          <input placeholder="Password" type="password" onChange={e => setPassword(e.target.value)} />
          {" "}
          <button onClick={login}>Login</button>
        </div>
      ) : (
        <div>
          <p>Logged in <button onClick={logout}>Logout</button></p>
          <h2>New Incident</h2>
          <input placeholder="Device name" value={form.device_name} onChange={e => setForm({ ...form, device_name: e.target.value })} />
          <br /><br />
          <input placeholder="Location" value={form.location} onChange={e => setForm({ ...form, location: e.target.value })} />
          <br /><br />
          <input placeholder="Incident type" value={form.incident_type} onChange={e => setForm({ ...form, incident_type: e.target.value })} />
          <br /><br />
          <input placeholder="Description" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
          <br /><br />
          <select value={form.severity} onChange={e => setForm({ ...form, severity: e.target.value })}>
            <option>low</option>
            <option>medium</option>
            <option>high</option>
            <option>critical</option>
          </select>
          {" "}
          <select value={form.status} onChange={e => setForm({ ...form, status: e.target.value })}>
            <option>open</option>
            <option>investigating</option>
            <option>resolved</option>
          </select>
          {" "}
          <button onClick={create}>Create</button>
        </div>
      )}

      {msg && <p style={{ color: "green" }}>{msg}</p>}

      <h2>All Incidents</h2>
      {incidents.map(i => (
        <div key={i._id} style={{ border: "1px solid #aaa", padding: 10, marginBottom: 8 }}>
          <b>{i.device_name}</b> | {i.incident_type} | {i.severity} | {i.status}
          <br />
          <small>{i.location} - {i.description}</small>
          {token && <button onClick={() => remove(i._id)} style={{ float: "right" }}>Delete</button>}
        </div>
      ))}
    </div>
  )
}
