const getBaseURL = () => {
  return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : '';
};

export const refreshInferrixToken = async () => {
  try {
    const refreshToken = localStorage.getItem('inferrix_refresh_token');
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const baseURL = getBaseURL();
    const response = await fetch(`${baseURL}/inferrix/refresh-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('jwt')}`
      },
      body: JSON.stringify({ refresh_token: refreshToken })
    });

    if (!response.ok) {
      throw new Error(`Failed to refresh token: ${response.status}`);
    }

    const data = await response.json();
    
    // Store the new tokens
    if (data.access_token) {
      localStorage.setItem('inferrix_access_token', data.access_token);
    }
    if (data.refresh_token) {
      localStorage.setItem('inferrix_refresh_token', data.refresh_token);
    }

    console.log(`Token refreshed using method: ${data.method || 'refresh'}`);
    return data.access_token;
  } catch (error) {
    console.error('Error refreshing Inferrix token:', error);
    throw error;
  }
};

export const getInferrixAccessToken = async () => {
  try {
    // First try to get the stored access token
    let accessToken = localStorage.getItem('inferrix_access_token');
    
    if (!accessToken) {
      // If no access token, try to refresh
      accessToken = await refreshInferrixToken();
    }
    
    return accessToken;
  } catch (error) {
    console.error('Error getting Inferrix access token:', error);
    throw error;
  }
};

export const makeInferrixApiCall = async (endpoint, options = {}) => {
  try {
    let accessToken = await getInferrixAccessToken();
    
    const url = `https://cloud.inferrix.com/api${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      'X-Authorization': `Bearer ${accessToken}`,
      ...options.headers
    };

    const response = await fetch(url, {
      ...options,
      headers
    });

    // If we get a 401, try to refresh the token and retry once
    if (response.status === 401) {
      console.log('Token expired, attempting refresh...');
      accessToken = await refreshInferrixToken();
      
      // Retry the request with the new token
      const retryResponse = await fetch(url, {
        ...options,
        headers: {
          ...headers,
          'X-Authorization': `Bearer ${accessToken}`
        }
      });
      
      if (!retryResponse.ok) {
        throw new Error(`API call failed: ${retryResponse.status} ${retryResponse.statusText}`);
      }
      
      return await retryResponse.json();
    }

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