import React, { useState, useEffect } from "react";
import Login from "./components/Login";
import DeviceDropdown from "./components/DeviceDropdown";
import Chat from "./components/Chat";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [devices, setDevices] = useState([]);
  const [selectedDeviceId, setSelectedDeviceId] = useState("");

  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      setIsAuthenticated(true);
      fetch('/inferrix/devices')
        .then(res => res.json())
        .then(data => setDevices(data.devices || []));
    }
  }, []);

  // Update handleLogin to accept the token argument
  const handleLogin = (token) => {
    setIsAuthenticated(true);
    // Optionally, store the token if needed
    fetch('/inferrix/devices')
      .then(res => res.json())
      .then(data => setDevices(data.devices || []));
  };

  const handleLogout = () => {
    localStorage.removeItem("jwt");
    setIsAuthenticated(false);
    setDevices([]);
    setSelectedDeviceId("");
  };

  return (
    <div className="App" style={{ minHeight: "100vh", background: "#f8fafc" }}>
      {isAuthenticated ? (
        <>
          <Chat
            devices={devices}
            selectedDeviceId={selectedDeviceId}
            onSelectDevice={setSelectedDeviceId}
            onLogout={handleLogout}
          />
        </>
      ) : (
        // Pass onLoginSuccess instead of onLogin
        <Login onLoginSuccess={handleLogin} />
      )}
    </div>
  );
}

export default App;
