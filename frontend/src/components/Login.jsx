import React, { useState } from "react";
import axios from "axios";

export default function Login({ onLoginSuccess }) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Clear any stored email on component mount
  React.useEffect(() => {
    // Clear any stored email from localStorage
    localStorage.removeItem("lastEmail");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("email");
    // Clear any stored form data
    sessionStorage.clear();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // Use localhost for local development, relative URL for production
      const baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
        ? 'http://localhost:8000' 
        : '';
      
      const res = await axios.post(`${baseURL}/login`, {
        email, // Use email as per backend
        password,
      });

      console.log("Login response:", res.data); // Debug log
      const token = res.data.access_token;
      const inferrixToken = res.data.inferrix_token;
      
      localStorage.setItem("jwt", token);
      if (inferrixToken) {
        localStorage.setItem("inferrix_token", inferrixToken);
        console.log("Inferrix token stored in localStorage");
      }
      
      console.log("JWT set in localStorage:", localStorage.getItem("jwt")); // Debug log
      onLoginSuccess(token); // Pass the real JWT up to App
    } catch (err) {
      console.error("Login error:", err);
      setError("❌ Invalid credentials or server issue.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded shadow-md w-96 border border-gray-200"
      >
        <h2 className="text-xl font-bold text-center text-blue-700 mb-6">
          Login to IntelliSustain
        </h2>

        <label className="block mb-2 text-sm font-medium">Email</label>
        <input
          type="email"
          className="w-full p-2 mb-4 border rounded"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label className="block mb-2 text-sm font-medium">Password</label>
        <input
          type="password"
          className="w-full p-2 mb-4 border rounded"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && <p className="text-red-500 text-sm mb-3">{error}</p>}

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded w-full"
        >
          Login
        </button>
      </form>
    </div>
  );
}
