// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [sessionId, setSessionId] = useState('');
  const [state, setState] = useState(null);
  const [newKey, setNewKey] = useState('');
  const [newValue, setNewValue] = useState('');

  const createSession = async () => {
    const res = await axios.post('http://localhost:8000/create_session');
    setSessionId(res.data.session_id);
    setState(null);
  };

  const fetchState = async () => {
    const res = await axios.get(`http://localhost:8000/state/${sessionId}`);
    setState(res.data);
  };

  const updateState = async () => {
    const update: Record<string, any> = {};  // ✅ 明确允许动态键
    update[newKey] = newValue;
    await axios.post(`http://localhost:8000/update_state/${sessionId}`, update);
    fetchState();
  };
  

  return (
    <div style={{ padding: 20 }}>
      <h1>TripWeaver Agent UI</h1>

      <button onClick={createSession}>Create Session</button>
      {sessionId && (
        <>
          <p>Session ID: <code>{sessionId}</code></p>
          <button onClick={fetchState}>Refresh State</button>

          <h2>Current State:</h2>
          <pre>{JSON.stringify(state, null, 2)}</pre>

          <h3>Update State</h3>
          <input placeholder="key" value={newKey} onChange={(e) => setNewKey(e.target.value)} />
          <input placeholder="value" value={newValue} onChange={(e) => setNewValue(e.target.value)} />
          <button onClick={updateState}>Update</button>
        </>
      )}
    </div>
  );
}

export default App;