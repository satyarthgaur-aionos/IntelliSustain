// API utilities for Inferrix token management

const getBaseURL = () => {
  return window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
    ? 'http://localhost:8000' 
    : '';
};

export const refreshInferrixToken = async () => {
  try {
    const refreshToken = localStorage.getItem('inferrix_refresh_token');
    if (!refreshToken) {
      console.warn('No refresh token found in localStorage');
      return null;
    }

    const baseURL = getBaseURL();
    const response = await fetch(`${baseURL}/inferrix/refresh-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (response.ok) {
      const data = await response.json();
      
      // Store the new refresh token
      if (data.refresh_token) {
        localStorage.setItem('inferrix_refresh_token', data.refresh_token);
      }
      
      return data.access_token;
    } else {
      console.error('Failed to refresh token:', response.status);
      return null;
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
    return null;
  }
};

export const getInferrixAccessToken = async () => {
  // Try to get a fresh token using refresh token
  const freshToken = await refreshInferrixToken();
  if (freshToken) {
    return freshToken;
  }
  
  // Fallback to stored token if refresh fails
  return localStorage.getItem('inferrix_access_token');
};

export const makeInferrixApiCall = async (endpoint, options = {}) => {
  try {
    const accessToken = await getInferrixAccessToken();
    if (!accessToken) {
      throw new Error('No access token available');
    }

    const response = await fetch(`https://cloud.inferrix.com/api${endpoint}`, {
      ...options,
      headers: {
        'X-Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (response.status === 401) {
      // Token expired, try to refresh and retry
      const newToken = await refreshInferrixToken();
      if (newToken) {
        const retryResponse = await fetch(`https://cloud.inferrix.com/api${endpoint}`, {
          ...options,
          headers: {
            'X-Authorization': `Bearer ${newToken}`,
            'Content-Type': 'application/json',
            ...options.headers,
          },
        });
        return retryResponse;
      }
    }

    return response;
  } catch (error) {
    console.error('Error making Inferrix API call:', error);
    throw error;
  }
}; 