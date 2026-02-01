import React, { useState } from "react";
import Dashboard from "./components/Dashboard";
import Login from "./components/Login";

function App() {
  const [user, setUser] = useState(null);

  return (
    <>
      {user ? (
        <Dashboard />
      ) : (
        <Login onLogin={(username) => setUser(username)} />
      )}
    </>
  );
}

export default App;
