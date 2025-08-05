// API Configuration for different environments
const API_CONFIG = {
  // Development (local)
  development: {
    baseURL: 'http://192.168.5.101:8000',
    mcpURL: 'http://192.168.5.101:8001'
  },
  
  // Production (Railway)
  production: {
    baseURL: window.location.origin.replace(':5173', ':8000'),
    mcpURL: window.location.origin.replace(':5173', ':8001')
  }
};

// Detect environment
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname.includes('railway');

const currentConfig = isDevelopment ? API_CONFIG.development : API_CONFIG.production;

export const API_BASE_URL = currentConfig.baseURL;
export const MCP_BASE_URL = currentConfig.mcpURL;

// API endpoints
export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/health`,
  login: `${API_BASE_URL}/login`,
  chat: `${API_BASE_URL}/chat/enhanced`,
  devices: `${API_BASE_URL}/intellisustain/devices`,
  mcp: `${MCP_BASE_URL}`
};

export default API_ENDPOINTS; 