import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import TextareaAutosize from "react-textarea-autosize";
import Logo from "./Logo";

// Voice Recognition Component
function VoiceRecognition({ onTranscript, isListening, setIsListening, isSupported, language }) {
  const recognitionRef = useRef(null);
  const [interimTranscript, setInterimTranscript] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const [pauseTimer, setPauseTimer] = useState(null);
  const [accumulatedTranscript, setAccumulatedTranscript] = useState("");

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition || window.mozSpeechRecognition || window.msSpeechRecognition;
    if (SpeechRecognition && isSupported) {
      recognitionRef.current = new SpeechRecognition();
      
      // Enhanced configuration for better accuracy and pause handling
      recognitionRef.current.continuous = true; // Keep listening after pauses
      recognitionRef.current.interimResults = true; // Enable interim results
      recognitionRef.current.lang = language; // Use specified language for better accent support
      
             // Additional settings for improved accuracy
       recognitionRef.current.maxAlternatives = 5; // Get more alternatives for better accuracy
       // Note: grammars property is not supported in all browsers, so we skip it
      
      // Enhanced pause handling - extend timeout for Indian English speakers
      if (recognitionRef.current.continuous !== undefined) {
        recognitionRef.current.continuous = true;
      }
      
      // Set longer timeout for pause handling (default is usually 10 seconds)
      // This helps with Indian English speakers who may pause while thinking
      if (recognitionRef.current.timeout !== undefined) {
        recognitionRef.current.timeout = 15000; // 15 seconds timeout
      }
      
      // Enhanced result handling with confidence scoring
      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        let highestConfidence = 0;
        let alternatives = [];

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const result = event.results[i];
          const transcript = result[0].transcript;
          const confidence = result[0].confidence || 0;
          
          if (result.isFinal) {
            finalTranscript += transcript;
            highestConfidence = Math.max(highestConfidence, confidence);
            
            // Collect alternatives for better suggestions
            if (result.length > 1) {
              for (let j = 1; j < Math.min(result.length, 3); j++) {
                alternatives.push({
                  text: result[j].transcript,
                  confidence: result[j].confidence || 0
                });
              }
            }
          } else {
            interimTranscript += transcript;
          }
        }

        setInterimTranscript(interimTranscript);
        setConfidence(highestConfidence);
        setSuggestions(alternatives);

                if (finalTranscript) {
          // Accumulate transcript to handle pauses - DON'T process immediately
          const newAccumulated = accumulatedTranscript + (accumulatedTranscript ? ' ' : '') + finalTranscript;
          setAccumulatedTranscript(newAccumulated);
          
          // Clear pause timer and set a new one
          if (pauseTimer) {
            clearTimeout(pauseTimer);
          }
          
          // Only process after a longer pause to allow for multiple speech segments
          const newPauseTimer = setTimeout(() => {
            // After 15 seconds of pause, process the accumulated transcript
            // This allows for multiple pauses while still processing eventually
            if (newAccumulated.trim()) {
              const processedTranscript = postProcessTranscript(newAccumulated);
              onTranscript(processedTranscript.trim());
              setIsListening(false);
              setInterimTranscript("");
              setConfidence(0);
              setSuggestions([]);
              setAccumulatedTranscript("");
            }
          }, 15000); // 15 second pause tolerance for multiple thinking pauses
          
          setPauseTimer(newPauseTimer);
        }
      };

      // Enhanced error handling with user guidance
      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        let errorMessage = '';
        
        switch (event.error) {
          case 'no-speech':
            errorMessage = 'No speech detected. Please speak clearly.';
            break;
          case 'audio-capture':
            errorMessage = 'Microphone not accessible. Please check permissions.';
            break;
          case 'not-allowed':
            errorMessage = 'Microphone access denied. Please allow microphone access.';
            break;
          case 'network':
            errorMessage = 'Network error. Please check your connection.';
            break;
          case 'service-not-allowed':
            errorMessage = 'Speech recognition service not available.';
            break;
          default:
            errorMessage = 'Speech recognition error. Please try again.';
        }
        
        // Show error message to user
        if (window.showVoiceError) {
          window.showVoiceError(errorMessage);
        }
        
        setIsListening(false);
        setInterimTranscript("");
        setConfidence(0);
        setSuggestions([]);
      };

      recognitionRef.current.onend = () => {
        // If we have accumulated transcript, process it
        if (accumulatedTranscript.trim()) {
          const processedTranscript = postProcessTranscript(accumulatedTranscript);
          onTranscript(processedTranscript.trim());
        }
        
        setIsListening(false);
        setInterimTranscript("");
        setConfidence(0);
        setSuggestions([]);
        setAccumulatedTranscript("");
        
        // Clear pause timer
        if (pauseTimer) {
          clearTimeout(pauseTimer);
          setPauseTimer(null);
        }
      };

      // Add speech start/end detection
      recognitionRef.current.onspeechstart = () => {
        console.log('Speech started');
      };

      recognitionRef.current.onspeechend = () => {
        console.log('Speech ended');
      };
    }
  }, [onTranscript, setIsListening, isSupported, language]);

  // Post-process transcript for better accuracy with Indian English accent support
  const postProcessTranscript = (transcript) => {
    let processed = transcript;
    
    // Enhanced corrections for Indian English accents and common misrecognitions
    const corrections = {
      // Common Indian English accent corrections
      'minor': 'minor',
      'miner': 'minor',
      'myner': 'minor',
      'meener': 'minor',
      'minar': 'minor',
      
      // Temperature variations
      'temperature': 'temperature',
      'temperatures': 'temperature',
      'temp': 'temperature',
      'temprature': 'temperature',
      'tempratures': 'temperature',
      'tempature': 'temperature',
      'tempatures': 'temperature',
      
      // Thermostat variations
      'thermostat': 'thermostat',
      'thermostats': 'thermostat',
      'thermostate': 'thermostat',
      'thermostates': 'thermostat',
      'thermo': 'thermostat',
      
      // Alarm variations
      'alarm': 'alarm',
      'alarms': 'alarm',
      'alerm': 'alarm',
      'alerms': 'alarm',
      'alert': 'alarm',
      'alerts': 'alarm',
      
      // Energy variations
      'energy': 'energy',
      'energies': 'energy',
      'energie': 'energy',
      'power': 'energy',
      'electricity': 'energy',
      
      // Consumption variations
      'consumption': 'consumption',
      'consumptions': 'consumption',
      'consume': 'consumption',
      'usage': 'consumption',
      'use': 'consumption',
      
      // Floor variations
      'floor': 'floor',
      'floors': 'floor',
      'flor': 'floor',
      'flors': 'floor',
      'level': 'floor',
      'levels': 'floor',
      
      // Room variations
      'room': 'room',
      'rooms': 'room',
      'rum': 'room',
      'rums': 'room',
      'chamber': 'room',
      'chambers': 'room',
      
      // Number variations (Indian English)
      'second': '2nd',
      'third': '3rd',
      'fourth': '4th',
      'fifth': '5th',
      'first': '1st',
      'to': '2nd',
      'tree': '3rd',
      'for': '4th',
      'fifth': '5th',
      
      // Time expressions
      'right now': 'right now',
      'rightnow': 'right now',
      'right-now': 'right now',
      'at present': 'at present',
      'atpresent': 'at present',
      'at-present': 'at present',
      'currently': 'currently',
      'now': 'now',
      'today': 'today',
      'past': 'past',
      'history': 'history',
      'previous': 'previous',
      'yesterday': 'yesterday',
      'last week': 'last week',
      'last month': 'last month',
      
      // Severity variations
      'highest': 'highest',
      'highest severity': 'highest severity',
      'highest-severity': 'highest severity',
      'critical': 'critical',
      'criticle': 'critical',
      'major': 'major',
      'warning': 'warning',
      'warn': 'warning',
      'info': 'info',
      'information': 'info',
      
      // Action words
      'show': 'show',
      'display': 'display',
      'get': 'get',
      'fetch': 'fetch',
      'check': 'check',
      'tell': 'tell',
      'give': 'give',
      
      // Question words (Indian English variations)
      'what is': 'what is',
      'whats': 'what is',
      'what\'s': 'what is',
      'what-is': 'what is',
      'how is': 'how is',
      'how\'s': 'how is',
      'how-is': 'how is',
      'tell me': 'tell me',
      'tell-me': 'tell me',
      'give me': 'give me',
      'give-me': 'give me',
      
             // Common Indian English filler words (remove these)
       'actually': '',
       'basically': '',
       'you know': '',
       'you-know': '',
       'like': '',
       'so': '',
       'okay': '',
       'ok': '',
       'right': '',
       'well': '',
       
       // Common thinking/speaking filler words (remove these)
       'hmm': '',
       'hmmm': '',
       'um': '',
       'uh': '',
       'ah': '',
       'aaaah': '',
       'aaaa': '',
       'err': '',
       'er': '',
       'erm': '',
       'uhm': '',
       'uhmm': '',
       'huh': '',
       'oh': '',
       'wow': '',
       'yeah': '',
       'yep': '',
       'nope': '',
       'no': '',
       'yes': '',
       'sure': '',
       'okay': '',
       'alright': '',
       'right': '',
       'well': '',
       'so': '',
       'like': '',
       'you know': '',
       'i mean': '',
       'i think': '',
       'i guess': '',
       'sort of': '',
       'kind of': '',
       'you see': '',
       'let me see': '',
       'let me think': '',
      
      // Device control variations
      'increase': 'increase',
      'decrease': 'decrease',
      'set': 'set',
      'change': 'set',
      'adjust': 'set',
      'turn': 'turn',
      'switch': 'turn',
      'on': 'on',
      'off': 'off',
      'up': 'up',
      'down': 'down',
      'high': 'high',
      'low': 'low',
      'medium': 'medium',
      'maximum': 'high',
      'minimum': 'low',
      
      // Degree variations
      'degree': 'degree',
      'degrees': 'degree',
      'deg': 'degree',
      'celsius': 'degree',
      'centigrade': 'degree'
    };

    // Apply corrections
    Object.entries(corrections).forEach(([incorrect, correct]) => {
      const regex = new RegExp(`\\b${incorrect}\\b`, 'gi');
      processed = processed.replace(regex, correct);
    });

    // Fix common punctuation issues
    processed = processed.replace(/\s+/g, ' '); // Remove extra spaces
    processed = processed.replace(/\s+([,.!?])/g, '$1'); // Fix spacing around punctuation
    
    // Remove multiple spaces and clean up
    processed = processed.trim();
    
    // Additional filler word removal using regex patterns
    const fillerPatterns = [
      /\b(?:hmm+|um+|uh+|ah+|err+|er+|erm+|uhm+|uhmm+|huh+|oh+|wow+)\b/gi,
      /\b(?:yeah|yep|nope|sure|alright|i mean|i think|i guess|sort of|kind of|you see|let me see|let me think)\b/gi,
      /\b(?:actually|basically|you know|like|so|okay|ok|right|well)\b/gi
    ];
    
    fillerPatterns.forEach(pattern => {
      processed = processed.replace(pattern, '');
    });
    
    // Clean up any remaining extra spaces after filler removal
    processed = processed.replace(/\s+/g, ' ').trim();
    
    // Log the correction for debugging
    if (processed !== transcript) {
      console.log(`Voice correction: "${transcript}" → "${processed}"`);
    }
    
    return processed;
  };

  const startListening = () => {
    if (recognitionRef.current && isSupported) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
        setInterimTranscript("");
        setConfidence(0);
        setSuggestions([]);
        setAccumulatedTranscript("");
        
        // Clear any existing pause timer
        if (pauseTimer) {
          clearTimeout(pauseTimer);
          setPauseTimer(null);
        }
      } catch (error) {
        console.error('Failed to start speech recognition:', error);
        setIsListening(false);
      }
    }
  };

  const stopListening = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      
      // Process any accumulated transcript immediately
      if (accumulatedTranscript.trim()) {
        const processedTranscript = postProcessTranscript(accumulatedTranscript);
        onTranscript(processedTranscript.trim());
      }
      
      setIsListening(false);
      setInterimTranscript("");
      setConfidence(0);
      setSuggestions([]);
      setAccumulatedTranscript("");
      
      // Clear pause timer
      if (pauseTimer) {
        clearTimeout(pauseTimer);
        setPauseTimer(null);
      }
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
      
      {/* Voice input status and guidance */}
      {isListening && (
        <div className="mt-2 text-center">
          <div className="text-xs sm:text-sm text-red-600 animate-pulse mb-1">
            🎤 Listening... Speak clearly
          </div>
          {confidence > 0 && (
            <div className="text-xs text-gray-500">
              Confidence: {Math.round(confidence * 100)}%
            </div>
          )}
                     {interimTranscript && (
             <div className="mt-1 text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded shadow max-w-xs">
               {interimTranscript}
             </div>
           )}
           {accumulatedTranscript && (
             <div className="mt-1 text-xs text-green-600 bg-green-50 px-2 py-1 rounded shadow max-w-xs border border-green-200">
               <div className="font-semibold">Accumulated:</div>
               {accumulatedTranscript}
             </div>
           )}
          {suggestions.length > 0 && (
            <div className="mt-1 text-xs text-blue-600">
              Alternatives: {suggestions.map(s => s.text).join(', ')}
            </div>
          )}
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
  const [showVoiceSettings, setShowVoiceSettings] = useState(false);

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

  // Define baseURL for API calls
  const baseURL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : '';

  // Check API status on mount
  useEffect(() => {
    async function checkApiStatus() {
      try {
        const jwt = localStorage.getItem("jwt");
        const res = await axios.get(`${baseURL}/health`, {
          headers: { Authorization: "Bearer " + jwt }
        });
        setApiStatus("connected");
      } catch (e) {
        setApiStatus("disconnected");
        console.error("API health check failed:", e);
      }
    }
    checkApiStatus();
  }, [baseURL]);

  // Fetch device list on mount
  useEffect(() => {
    async function fetchDevices() {
      try {
        const jwt = localStorage.getItem("jwt");
        const inferrixToken = localStorage.getItem("inferrix_token");
        const res = await axios.get(`${baseURL}/inferrix/devices`, {
          headers: { 
            Authorization: "Bearer " + jwt,
            "X-Inferrix-Token": inferrixToken
          }
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
      const inferrixToken = localStorage.getItem("inferrix_token");
      if (!jwt) {
        throw new Error("No authentication token found");
      }
      const controller = new AbortController();
      setAbortController(controller);
      
              const res = await axios.post(
          `${baseURL}/chat/enhanced`,
        {
          query: mappedQuery,
          user,
          device: selectedDevice
        },
        {
          headers: {
            Authorization: "Bearer " + jwt,
            "X-Inferrix-Token": inferrixToken
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
              <div className="flex flex-col items-center gap-1">
                <VoiceRecognition
                  onTranscript={(transcript) => setQuery(transcript)}
                  isListening={isListening}
                  setIsListening={setIsListening}
                  isSupported={isSupported}
                  language={language} // Pass language prop
                />
                {isSupported && (
                  <button
                    onClick={() => setShowVoiceSettings(!showVoiceSettings)}
                    className="text-xs text-gray-500 hover:text-gray-700 transition"
                    title="Voice settings"
                  >
                    ⚙️
                  </button>
                )}
              </div>
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
                         {/* Voice settings only */}
             {!isListening && isSupported && showVoiceSettings && (
               <div className="mt-2 text-center">
                 <div className="mt-3 p-2 bg-gray-50 rounded border">
                   <div className="text-xs font-semibold text-gray-700 mb-2">Voice Settings:</div>
                   <div className="flex items-center gap-2 text-xs">
                     <label htmlFor="voice-language" className="text-gray-600">Language:</label>
                     <select
                       id="voice-language"
                       value={language}
                       onChange={(e) => setLanguage(e.target.value)}
                       className="border rounded px-1 py-0.5 text-xs"
                     >
                       <option value="en-IN">English (India)</option>
                       <option value="en-US">English (US)</option>
                       <option value="en-GB">English (UK)</option>
                       <option value="hi-IN">Hindi (India)</option>
                     </select>
                   </div>
                   <div className="text-xs text-gray-500 mt-1">
                     Current: {language === 'en-IN' ? 'English (India)' : 
                              language === 'en-US' ? 'English (US)' : 
                              language === 'en-GB' ? 'English (UK)' : 
                              language === 'hi-IN' ? 'Hindi (India)' : language}
                   </div>
                 </div>
               </div>
             )}
          </div>
        </div>
      </main>
    </div>
  );
}
