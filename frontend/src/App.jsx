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
    const inferrixToken = localStorage.getItem("inferrix_token");
    if (jwt && inferrixToken) {
      setIsAuthenticated(true);
      // Use localhost for local development, relative URL for production
      const baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:8000' 
        : '';
      
      fetch(`${baseURL}/inferrix/devices`, {
        headers: {
          'Authorization': `Bearer ${jwt}`,
          'X-Inferrix-Token': inferrixToken
        }
      })
        .then(res => res.json())
        .then(data => setDevices(data.devices || []))
        .catch(error => console.error('Error fetching devices:', error));
    }
  }, []);

  // Update handleLogin to accept the token argument
  const handleLogin = (token) => {
    setIsAuthenticated(true);
    const inferrixToken = localStorage.getItem("inferrix_token");
    // Use localhost for local development, relative URL for production
    const baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
      ? 'http://localhost:8000' 
      : '';
    
    // Fetch devices with proper authentication
    fetch(`${baseURL}/inferrix/devices`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-Inferrix-Token': inferrixToken
      }
    })
      .then(res => res.json())
      .then(data => setDevices(data.devices || []))
      .catch(error => console.error('Error fetching devices:', error));
  };

  const handleLogout = () => {
    // Clear all tokens from localStorage
    localStorage.removeItem("jwt");
    localStorage.removeItem("inferrix_token");
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
