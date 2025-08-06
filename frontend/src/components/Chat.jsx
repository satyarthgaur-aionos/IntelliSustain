import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import TextareaAutosize from "react-textarea-autosize";
import Logo from "./Logo";
import ReactMarkdown from 'react-markdown';
import DynamicTable from './DynamicTable';

const suggestions = [
  // Weather and Risk Analysis (New)
  "What is the weather prediction in Mumbai for tomorrow?",
  "What HVAC risks if it rains in Mumbai this week?",
  "Show me weather forecast for Delhi this week",
  "What are the lighting risks if temperature drops in Bangalore?",
  
  // Hotel-Specific Scenarios (New)
  "Increase temperature by 2 degrees in room 101 for the next 3 hours",
  "Optimize energy usage in guest rooms during low occupancy",
  "Schedule preventive maintenance for elevator equipment on floor 3",
  "Optimize room comfort for deluxe suite guests",
  "Analyze energy consumption patterns for the last month",
  "Get alarms for device 300186 with status ACTIVE",
  "Show attributes for device 150002",
  
  // New Conversational AI Scenarios
  "Turn off HVAC and dim lights in the east wing on Saturday and Sunday. Send me a report Monday.",
  "Lower the temperature by 2 degrees in Conference Room B for the next 3 hours.",
  "Are any HVAC or lighting systems likely to fail in the next 7 days?",
  "How much carbon emissions did we reduce this week? Are we on track for our Q3 target?",
  "What are the least used restrooms on the 3rd floor today?",
  "Why is the east wing warm and noisy today?",
  
  // Existing Prompts
  "Show me all critical alarms for Tower A",
  "Acknowledge the high temperature alarm for Device X",
  "List of all active devices",
  "List devices with low battery",
  "Show top 3 alarm types",
  "Show temperature",
  "Check device health",
  "Show humidity",
  "Check if device is online",
  "Show battery level"
];

function AlarmTable({ alarms }) {
  return (
    <table className="min-w-full text-sm border mt-2">
      <thead>
        <tr className="bg-gray-100">
          <th className="px-2 py-1">Time</th>
          <th className="px-2 py-1">Device</th>
          <th className="px-2 py-1">Type</th>
          <th className="px-2 py-1">Severity</th>
          <th className="px-2 py-1">Status</th>
        </tr>
      </thead>
      <tbody>
        {alarms.map((a, i) => (
          <tr key={i} className="border-t">
            <td className="px-2 py-1">{a.createdTime || a.time || "-"}</td>
            <td className="px-2 py-1">{a.originatorName || a.device || "-"}</td>
            <td className="px-2 py-1">{a.type || a.name || "-"}</td>
            <td className="px-2 py-1">
              <span className={`px-2 py-1 rounded text-xs font-bold ${
                a.severity === "CRITICAL"
                  ? "bg-red-500 text-white"
                  : a.severity === "MAJOR"
                  ? "bg-yellow-400 text-black"
                  : "bg-gray-200 text-gray-800"
              }`}>
                {a.severity || "-"}
              </span>
            </td>
            <td className="px-2 py-1">{a.status || a.state || "-"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Helper function to detect if text contains a Markdown table
function isMarkdownTable(text) {
  const lines = text.trim().split('\n');
  if (lines.length < 3) return false;
  
  // Find the table start line (look for line that starts with |)
  let tableStartIndex = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim().startsWith('|')) {
      tableStartIndex = i;
      break;
    }
  }
  
  if (tableStartIndex === -1) return false;
  
  // Check if we have enough lines after table start
  if (tableStartIndex + 2 >= lines.length) return false;
  
  // Check if next line contains separator (---)
  const separatorLine = lines[tableStartIndex + 1];
  if (!separatorLine.includes('---')) return false;
  
  // Check if we have at least one data row
  const dataLines = lines.slice(tableStartIndex + 2);
  const hasDataRows = dataLines.some(line => 
    line.trim().startsWith('|') && 
    line.split('|').some(cell => cell.trim().length > 0)
  );
  
  // Debug logging (commented out for production)
  // console.log('Table detection:', {
  //   text: text.substring(0, 200) + '...',
  //   linesCount: lines.length,
  //   tableStartIndex,
  //   firstLineStartsWithPipe: lines[tableStartIndex]?.startsWith('|'),
  //   separatorLineHasSeparator: separatorLine.includes('---'),
  //   hasDataRows,
  //   dataLines: dataLines.slice(0, 2),
  //   tableStartLine: lines[tableStartIndex],
  //   separatorLine: separatorLine,
  //   firstDataLine: dataLines[0] || 'N/A'
  // });
  
  return hasDataRows;
}

function MarkdownTable({ markdown }) {
  // Enhanced parser for Markdown tables with better styling
  const lines = markdown.trim().split('\n');
  
  // More robust table detection
  const isTable = isMarkdownTable(markdown) || markdown.includes('| Time |') || 
                  (lines.length >= 3 && lines[0].includes('|') && lines[1].includes('---'));
  
  if (!isTable) return <pre>{markdown}</pre>;
  
  // Find the table start line
  let tableStartIndex = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim().startsWith('|')) {
      tableStartIndex = i;
      break;
    }
  }
  
  if (tableStartIndex === -1) return <pre>{markdown}</pre>;
  
  // Parse headers (table start line) - filter out empty headers
  const headers = lines[tableStartIndex].split('|').map(h => h.trim()).filter(h => h.length > 0);
  
  // Skip the separator line (next line with ---)
  const dataLines = lines.slice(tableStartIndex + 2);
  
  // Parse data rows and align with headers
  const rows = dataLines
    .filter(line => line.trim().startsWith('|') && line.trim().length > 1)
    .map(line => {
      const cells = line.split('|').map(cell => cell.trim());
      // Ensure we have the same number of cells as headers
      const alignedCells = [];
      for (let i = 0; i < headers.length; i++) {
        const cellValue = cells[i + 1] || '-'; // Skip first empty cell, use '-' for missing cells
        alignedCells.push(cellValue === '' ? '-' : cellValue);
      }
      return alignedCells;
    })
    .filter(row => row.some(cell => cell !== '-' && cell.length > 0)); // Filter out completely empty rows
  
  // Use the DynamicTable component for proper HTML table rendering
  return <DynamicTable data={rows} headers={headers} />;
}

// Helper function to detect weather and risk messages
function getMessageStyle(text) {
  if (text.startsWith('🌤️')) {
    return 'bg-blue-50 border-l-4 border-blue-400 text-blue-900';
  } else if (text.startsWith('🌦️')) {
    return 'bg-orange-50 border-l-4 border-orange-400 text-orange-900';
  }
  return 'bg-gray-100 text-gray-900';
}

// Voice Recognition Component
function VoiceRecognition({ onTranscript, isListening, setIsListening, isSupported }) {
  const recognitionRef = useRef(null);
  const [interimTranscript, setInterimTranscript] = useState("");

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    if (SpeechRecognition && isSupported) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true; // Keep listening after pauses
      recognitionRef.current.interimResults = true; // Enable interim results
      recognitionRef.current.lang = 'en-IN'; // Use Indian English for better accent support

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
  }, [onTranscript, setIsListening, isSupported]);

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

export default function Chat({ devices, selectedDeviceId, onSelectDevice, onLogout }) {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [deviceSearch, setDeviceSearch] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const messagesEndRef = useRef(null);
  const [isListening, setIsListening] = useState(false);
  const [isSupported, setIsSupported] = useState(false);

  // Check browser compatibility for speech recognition
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    setIsSupported(!!SpeechRecognition);
    if (!SpeechRecognition) {
      console.warn('Speech recognition not supported in this browser');
    }
  }, []);

  // Extract user email from JWT on mount
  useEffect(() => {
    const jwt = localStorage.getItem("jwt");
    if (jwt) {
      try {
        const payload = JSON.parse(atob(jwt.split('.')[1]));
        setUserEmail(payload.sub || "");
      } catch (e) {
        console.error("Failed to parse JWT:", e);
        setUserEmail("");
      }
    }
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSend = async () => {
    if (!query.trim()) return;
    setLoading(true);
    setError("");
    setMessages((msgs) => [...msgs, { sender: userEmail, text: query, device: selectedDeviceId }]);
    try {
              const jwt = localStorage.getItem("jwt");
        // Use localhost for local development, relative URL for production
        const baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
          ? 'http://localhost:8000' 
          : '';
        
        const res = await axios.post(
          `${baseURL}/chat/enhanced`,
        {
          query,           // the user's query string
          user: userEmail, // dynamically extracted user email
          device: selectedDeviceId || null
        },
        { headers: { Authorization: "Bearer " + jwt } }
      );
      setMessages((msgs) => [...msgs, { sender: "AI", text: res.data.response }]);
      setQuery("");
    } catch (e) {
      setError("❌ Failed to get response from server. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // Filtered device list for search
  const filteredDevices = devices.filter(d =>
    (d.name && d.name.toLowerCase().includes(deviceSearch.toLowerCase())) ||
    (d.id && d.id.toLowerCase().includes(deviceSearch.toLowerCase()))
  );

  return (
    <div className="flex flex-col h-screen w-full max-w-7xl mx-auto">
      {/* Header Bar */}
      <div className="bg-white p-4 flex justify-between items-center rounded-t-lg shadow-sm">
        <div className="flex items-center gap-4">
          <Logo className="h-10 w-auto" />
          <div className="flex flex-col">
            <h1 className="text-2xl font-bold text-gray-800">Smart Building AI</h1>
            <p className="text-sm text-gray-600">Your intelligent building assistant</p>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <button onClick={onLogout} className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors duration-200">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6A2.25 2.25 0 005.25 5.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M18 12H9m0 0l3-3m-3 3l3 3" />
            </svg>
            Logout
          </button>
          {userEmail && (
            <div className="text-gray-800 text-sm font-medium mt-1">{userEmail}</div>
          )}
        </div>
      </div>
      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto min-h-[300px] bg-gray-50 rounded-b-lg shadow-lg p-4">
        {messages.length === 0 && <div className="text-center text-gray-400">No messages yet.</div>}
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === userEmail ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`flex flex-col max-w-[90%] ${msg.sender === userEmail ? 'items-end' : 'items-start'}`}>
              <div className={`flex items-start gap-2 p-3 rounded-lg ${msg.sender === userEmail ? 'bg-blue-100 text-blue-900' : 'bg-white text-gray-800 border border-gray-200'}`}>
                <span className="text-xs font-bold mt-1">{msg.sender === userEmail ? 'You' : 'AI'}:</span> 
                <div className="flex-1">
                  {isMarkdownTable(msg.text) || msg.text.includes('| Time |') ? (
                    <div>
                      {(() => {
                        const lines = msg.text.split('\n');
                        let tableStartIndex = -1;
                        for (let i = 0; i < lines.length; i++) {
                          if (lines[i].trim().startsWith('|')) {
                            tableStartIndex = i;
                            break;
                          }
                        }
                        
                        if (tableStartIndex > 0) {
                          // There's text before the table
                          const textBeforeTable = lines.slice(0, tableStartIndex).join('\n');
                          const tablePart = lines.slice(tableStartIndex).join('\n');
                          return (
                            <>
                              <ReactMarkdown>{textBeforeTable}</ReactMarkdown>
                              <MarkdownTable markdown={tablePart} />
                            </>
                          );
                        } else {
                          // Table starts from the beginning
                          return <MarkdownTable markdown={msg.text} />;
                        }
                      })()}
                    </div>
                  ) : (
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  )}
                </div>
              </div>
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      {error && <div className="text-red-500 text-sm mb-4">{error}</div>}
      {/* Input Area */}
      <div className="p-4 bg-white shadow-lg rounded-b-lg flex items-center justify-center gap-4">
        <TextareaAutosize
          minRows={2}
          maxRows={6}
          value={query}
          onChange={e => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your message..."
          className="flex-1 p-3 rounded-full border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={loading || !query.trim()}
          className="p-3 rounded-full bg-blue-600 text-white hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Send message"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
        <VoiceRecognition onTranscript={setQuery} isListening={isListening} setIsListening={setIsListening} isSupported={isSupported} />
      </div>
    </div>
  );
}
