const getBaseURL = () => {
  return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : '';
};

export const getInferrixToken = () => {
  // Simply get the token from localStorage
  const token = localStorage.getItem('inferrix_token');
  if (!token) {
    throw new Error('No Inferrix token available. Please log in again.');
  }
  return token;
};

export const makeInferrixApiCall = async (endpoint, options = {}) => {
  try {
    const token = getInferrixToken();
    
    const url = `https://cloud.inferrix.com/api${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      'X-Authorization': `Bearer ${token}`,
      ...options.headers
    };

    const response = await fetch(url, {
      ...options,
      headers
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error making Inferrix API call:', error);
    throw error;
  }
};

// Convenience functions for common API calls
export const getDevices = async () => {
  return await makeInferrixApiCall('/devices');
};

export const getAlarms = async (page = 0, pageSize = 100) => {
  return await makeInferrixApiCall(`/alarms?page=${page}&pageSize=${pageSize}`);
};

export const getTelemetry = async (entityType, entityId, scope) => {
  return await makeInferrixApiCall(`/plugins/telemetry/${entityType}/${entityId}/timeseries/${scope}`);
};

export const sendControlCommand = async (entityType, entityId, command) => {
  return await makeInferrixApiCall(`/plugins/telemetry/${entityType}/${entityId}/timeseries/control`, {
    method: 'POST',
    body: JSON.stringify(command)
  });
}; 