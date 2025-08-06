import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import TextareaAutosize from "react-textarea-autosize";
import Logo from "./Logo";

// Voice Recognition Component
function VoiceRecognition({ onTranscript, isListening, setIsListening, isSupported, language }) {
  const recognitionRef = useRef(null);
  const [interimTranscript, setInterimTranscript] = useState("");

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    if (SpeechRecognition && isSupported) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true; // Keep listening after pauses
      recognitionRef.current.interimResults = true; // Enable interim results
      recognitionRef.current.lang = language; // Use Indian English for better accent support

      recognitionRef.current.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          transcript += event.results[i][0].transcript;
        }
        setInterimTranscript(transcript);
        if (event.results[event.results.length - 1].isFinal) {
          onTranscript(transcript.trim());
          setIsListening(false);
          setInterimTranscript("");
        }
      };
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setInterimTranscript("");
      };
      recognitionRef.current.onend = () => {
        setIsListening(false);
        setInterimTranscript("");
      };
    }
  }, [onTranscript, setIsListening, isSupported, language]);

  const startListening = () => {
    if (recognitionRef.current && isSupported) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        setInterimTranscript("");
      } catch (error) {
        console.error('Failed to start speech recognition:', error);
        setIsListening(false);
      }
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
      setInterimTranscript("");
    }
  };

  if (!isSupported) {
    return null;
  }

  return (
    <div className="flex flex-col items-center">
      <button
        onClick={isListening ? stopListening : startListening}
        className={`p-2 rounded-full transition-all duration-200 ${
          isListening 
            ? 'bg-red-500 text-white animate-pulse' 
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
        title={isListening ? "Stop listening" : "Start voice input"}
        aria-label={isListening ? "Stop voice input" : "Start voice input"}
      >
        {isListening ? (
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5.25 7.5A2.25 2.25 0 017.5 5.25h9a2.25 2.25 0 012.25 2.25v9a2.25 2.25 0 01-2.25 2.25h-9a2.25 2.25 0 01-2.25-2.25v-9z" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" />
          </svg>
        )}
      </button>
      {isListening && interimTranscript && (
        <div className="mt-1 text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded shadow">
          {interimTranscript}
        </div>
      )}
    </div>
  );
}

export default function VoiceChat() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [deviceList, setDeviceList] = useState([]);
  const [selectedDevice, setSelectedDevice] = useState("");
  const [deviceSearch, setDeviceSearch] = useState("");
  const [user, setUser] = useState("");
  const [apiStatus, setApiStatus] = useState("checking");
  const messagesEndRef = useRef(null);
  const [abortController, setAbortController] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);
  const [language, setLanguage] = useState('en-IN'); // Add language state

  // Check browser compatibility for speech recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    setIsSupported(!!SpeechRecognition);
    
    if (!SpeechRecognition) {
      console.warn('Speech recognition not supported in this browser');
    }
  }, []);

  // Extract user from JWT on mount
  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      try {
        const payload = JSON.parse(atob(jwt.split('.')[1]));
        setUser(payload.sub || "User");
      } catch (e) {
        console.error("Failed to parse JWT:", e);
        setUser("User");
      }
    }
  }, []);

  // Check API status on mount
  useEffect(() => {
    async function checkApiStatus() {
      try {
        const jwt = localStorage.getItem("jwt");
        const res = await axios.get("/health", {
          headers: { Authorization: "Bearer " + jwt }
        });
        setApiStatus("connected");
      } catch (e) {
        setApiStatus("disconnected");
        console.error("API health check failed:", e);
      }
    }
    checkApiStatus();
  }, []);

  // Fetch device list on mount
  useEffect(() => {
    async function fetchDevices() {
      try {
        const jwt = localStorage.getItem("jwt");
        const res = await axios.get("/inferrix/devices", {
          headers: { Authorization: "Bearer " + jwt }
        });
        setDeviceList(res.data.devices || []);
      } catch (e) {
        console.error("Failed to fetch device list", e);
        if (e.response?.status === 401) {
          handleLogout();
        }
      }
    }
    fetchDevices();
  }, []);

  // Filtered device list for autocomplete
  const filteredDevices = deviceList.filter(d =>
    (d.name && d.name.toLowerCase().includes(deviceSearch.toLowerCase())) ||
    (d.id && d.id.toLowerCase().includes(deviceSearch.toLowerCase()))
  );

  const handleLogout = () => {
    localStorage.removeItem("jwt");
    window.location.reload();
  };

  const handleSend = async () => {
    if (!query.trim()) return;
    setError("");
    
    let selectedDeviceName = "";
    if (selectedDevice) {
      const deviceObj = deviceList.find(d => d.id?.id === selectedDevice);
      selectedDeviceName = deviceObj?.name || selectedDevice;
    }
    
    let mappedQuery = query;
    if (selectedDevice && selectedDeviceName) {
      const deviceMentioned = /\b(device|tower|sensor|thermostat)\b/i.test(query);
      if (!deviceMentioned) {
        mappedQuery = `${query} for ${selectedDeviceName}`;
      } else {
        mappedQuery = query.replace(/\b(device|tower|sensor|thermostat)\b/gi, selectedDeviceName);
      }
    }
    
    const newMessage = { from: "user", text: query };
    setMessages((prev) => [...prev, newMessage]);
    setLoading(true);
    
    try {
      const jwt = localStorage.getItem("jwt");
      if (!jwt) {
        throw new Error("No authentication token found");
      }
      const controller = new AbortController();
      setAbortController(controller);
      
      const res = await axios.post(
        "/chat/enhanced",
        {
          query: mappedQuery,
          user,
          device: selectedDevice
        },
        {
          headers: {
            Authorization: "Bearer " + jwt,
          },
          signal: controller.signal
        }
      );
      
      let response = res.data.response;
      if (typeof response === "object" && response !== null && response.result) {
        response = response.result;
      }
      
      if (typeof response !== "string" || response.trim() === "") {
        response = "No data found or unable to answer your query.";
      }
      
      let isAlarmTable = false;
      let alarms = [];
      try {
        const parsed = JSON.parse(response);
        if (Array.isArray(parsed) && parsed.length && parsed[0].severity) {
          isAlarmTable = true;
          alarms = parsed;
        }
      } catch {}
      
      setMessages((prev) => [
        ...prev,
        { from: "bot", text: response, isAlarmTable, alarms },
      ]);
    } catch (err) {
      if (axios.isCancel && err.code === 'ERR_CANCELED') {
        setMessages((prev) => [
          ...prev,
          { from: "bot", text: "❌ Request cancelled by user." },
        ]);
      } else if (err.response?.status === 401) {
        setError("Session expired. Please log in again.");
        handleLogout();
      } else {
        setError("❌ Error processing request. Please try again.");
        setMessages((prev) => [
          ...prev,
          { from: "bot", text: "❌ Error processing request. Please try again." },
        ]);
      }
    } finally {
      setQuery("");
      setLoading(false);
      setAbortController(null);
    }
  };

  const handleCancel = () => {
    if (abortController) {
      abortController.abort();
      setAbortController(null);
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar - Hidden on mobile */}
      <aside className="hidden sm:flex w-20 bg-blue-900 flex-col items-center py-6">
        <Logo className="h-8" />
      </aside>
      
      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col items-center justify-center relative">
        <div className="w-full max-w-2xl bg-white rounded-xl shadow-lg flex flex-col h-[90vh] mx-4 sm:mx-0">
          {/* API Status Banner */}
          {apiStatus === "disconnected" && (
            <div className="bg-yellow-100 text-yellow-700 p-2 rounded-t-xl border-b border-yellow-300 z-10 text-sm">
              ⚠️ IntelliSustain API is currently unavailable. Some features may not work.
            </div>
          )}
          
          {/* Error Banner */}
          {error && (
            <div className="bg-red-100 text-red-700 p-2 rounded-t-xl border-b border-red-300 z-10 text-sm">
              {error}
            </div>
          )}
          
          {/* Header with logo and logout */}
          <header className="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Logo className="h-10 w-auto" />
              <span className="text-2xl font-extrabold text-blue-900 tracking-tight">IntelliSustain AI Agent</span>
            </div>
            <div className="flex flex-col items-end">
              <button
                onClick={handleLogout}
                className="ml-auto flex items-center gap-1 sm:gap-2 bg-red-600 text-white px-2 sm:px-4 py-1 sm:py-2 rounded shadow hover:bg-red-700 transition text-xs sm:text-sm"
                title="Logout"
                aria-label="Logout"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 sm:w-5 sm:h-5">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m-6-3h12m0 0l-3-3m3 3l-3 3" />
                </svg>
                <span className="hidden sm:inline">Logout</span>
              </button>
              {user && (
                <div className="text-blue-900 text-xs sm:text-sm font-semibold text-right w-full" style={{background: '#f8fafc', color: '#1e40af', marginTop: 6}}>
                  {user}
                </div>
              )}
            </div>
          </header>
          
          {/* User info */}
          {user && (
            <div className="text-blue-900 text-xs sm:text-sm px-4 sm:px-6 pt-2 pb-1 font-semibold text-right w-full" style={{background: '#f8fafc'}}>
              {user}
            </div>
          )}
          
          {/* Device Selection - Responsive */}
          <div className="px-4 sm:px-6 pt-4 pb-2 flex flex-col sm:flex-row items-start sm:items-center gap-2">
            <label htmlFor="device-search" className="font-semibold text-blue-900 text-sm">Device:</label>
            <div className="flex flex-col sm:flex-row gap-2 w-full sm:w-auto">
              <input
                id="device-search"
                type="text"
                className="border rounded px-2 py-1 text-sm sm:text-base w-full sm:w-auto"
                placeholder="Search device name or ID..."
                value={deviceSearch}
                onChange={e => {
                  setDeviceSearch(e.target.value);
                  setSelectedDevice("");
                }}
                autoComplete="off"
                aria-label="Search devices"
              />
              <select
                id="device-select"
                className={`border rounded px-2 py-1 text-sm sm:text-base w-full sm:w-auto ${selectedDevice ? 'bg-blue-50 border-blue-300' : ''}`}
                value={selectedDevice}
                onChange={e => setSelectedDevice(e.target.value)}
                aria-label="Select device"
              >
                <option value="">-- Select Device (optional) --</option>
                {filteredDevices.map((d, i) => (
                  <option key={i} value={d.id?.id}>
                    {d.name}{d.id?.id ? ` (${d.id.id})` : ""}
                  </option>
                ))}
              </select>
            </div>
            {selectedDevice && (
              <div className="flex items-center gap-1 text-xs sm:text-sm text-green-700 bg-green-50 px-2 py-1 rounded border border-green-200">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-3 h-3 sm:w-4 sm:h-4">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="font-medium">
                  {deviceList.find(d => d.id?.id === selectedDevice)?.name || selectedDevice}
                </span>
              </div>
            )}
          </div>
          
          {/* Chat Messages */}
          <div className="flex-1 min-h-0 max-h-[60vh] overflow-y-auto p-4 sm:p-6 space-y-4 bg-gray-50">
            {messages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <div className="text-3xl sm:text-4xl mb-4">🤖</div>
                <p className="text-sm sm:text-base">Welcome to IntelliSustain AI Agent!</p>
                <p className="text-xs sm:text-sm mt-2">Ask me about alarms, devices, telemetry, weather forecasts, or facility risks.</p>
                <p className="text-xs text-blue-600 mt-2">🎤 Try voice input for hands-free operation!</p>
              </div>
            )}
            
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`flex items-end mb-2 ${msg.from === "user" ? "justify-end" : "justify-start"}`}
              >
                {msg.from === "bot" && (
                  <div className="w-6 h-6 sm:w-8 sm:h-8 bg-blue-900 text-white flex items-center justify-center rounded-full mr-2">
                    <span role="img" aria-label="bot" className="text-xs sm:text-sm">🤖</span>
                  </div>
                )}
                <div
                  className={`max-w-[85%] sm:max-w-[70%] p-3 sm:p-4 rounded-2xl shadow text-sm sm:text-lg whitespace-pre-line
                    ${msg.from === "user"
                      ? "bg-blue-600 text-white rounded-br-none"
                      : msg.from === "bot" && (msg.text.startsWith('🌤️') || msg.text.startsWith('🌦️'))
                      ? `rounded-bl-none ${msg.text.startsWith('🌤️') ? 'bg-blue-50 border-l-4 border-blue-400 text-blue-900' : 'bg-orange-50 border-l-4 border-orange-400 text-orange-900'}`
                      : "bg-gray-100 text-gray-900 rounded-bl-none"}
                  `}
                >
                  {msg.text}
                </div>
                {msg.from === "user" && (
                  <div className="w-6 h-6 sm:w-8 sm:h-8 bg-gray-300 text-blue-900 flex items-center justify-center rounded-full ml-2">
                    <span role="img" aria-label="user" className="text-xs sm:text-sm">🧑</span>
                  </div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="flex items-end mb-2 justify-start">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-blue-900 text-white flex items-center justify-center rounded-full mr-2">
                  <span role="img" aria-label="bot" className="text-xs sm:text-sm">🤖</span>
                </div>
                <div className="bg-gray-100 text-gray-500 p-3 rounded-2xl shadow max-w-[85%] sm:max-w-[70%] flex items-center gap-2">
                  <div className="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-blue-600"></div>
                  <span className="text-sm sm:text-base">AI is thinking...</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          {/* Input with Voice Support */}
          <div className="p-4 border-t bg-white rounded-b-xl">
            <div className="flex items-center gap-2">
              <TextareaAutosize
                minRows={1}
                maxRows={3}
                className="flex-1 p-2 border rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm sm:text-base bg-gray-50 shadow-sm"
                placeholder="Type your message or use voice input..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                aria-label="Chat input"
              />
              <VoiceRecognition
                onTranscript={(transcript) => setQuery(transcript)}
                isListening={isListening}
                setIsListening={setIsListening}
                isSupported={isSupported}
                language={language} // Pass language prop
              />
              <button
                onClick={handleSend}
                className="bg-blue-600 text-white px-3 sm:px-4 py-2 rounded shadow hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-1 sm:gap-2"
                disabled={loading || !query.trim()}
                style={{ height: 48 }}
                aria-label="Send message"
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-3 w-3 sm:h-4 sm:w-4 border-b-2 border-white"></div>
                    <span className="hidden sm:inline">Sending...</span>
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-4 h-4 sm:w-5 sm:h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
                    </svg>
                    <span className="hidden sm:inline">Send</span>
                  </>
                )}
              </button>
              {loading && (
                <button
                  onClick={handleCancel}
                  className="bg-red-600 text-white px-2 sm:px-3 py-2 rounded shadow hover:bg-red-700 transition text-xs sm:text-sm"
                  aria-label="Stop AI"
                  title="Stop AI"
                >
                  <span className="hidden sm:inline">Stop</span>
                  <span className="sm:hidden">✕</span>
                </button>
              )}
            </div>
            {/* Voice input status */}
            {isListening && (
              <div className="mt-2 text-center text-xs sm:text-sm text-red-600 animate-pulse">
                🎤 Listening... Speak now
              </div>
            )}
            {/* Browser compatibility notice */}
            {!isSupported && (
              <div className="mt-2 text-center text-xs text-gray-500">
                💡 Voice input not supported in this browser. Try Chrome, Edge, or Firefox.
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
