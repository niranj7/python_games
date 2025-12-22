# React.js Connection Endpoint Configuration

This document provides comprehensive guidance on configuring React.js applications to connect to backend API endpoints.

## Table of Contents
- [Environment Variables](#environment-variables)
- [API Endpoint Configuration](#api-endpoint-configuration)
- [Development Setup](#development-setup)
- [Production Configuration](#production-configuration)
- [Example Implementation](#example-implementation)

## Environment Variables

### Creating Environment Files

Create environment-specific configuration files in your React.js project root:

#### `.env.development`
```env
REACT_APP_API_BASE_URL=http://localhost:3001/api
REACT_APP_WS_URL=ws://localhost:3001
REACT_APP_ENVIRONMENT=development
```

#### `.env.production`
```env
REACT_APP_API_BASE_URL=https://api.yourdomain.com/api
REACT_APP_WS_URL=wss://api.yourdomain.com
REACT_APP_ENVIRONMENT=production
```

#### `.env.local` (optional, for local overrides)
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
```

**Important Notes:**
- Environment variables in React must be prefixed with `REACT_APP_` to be accessible in the browser
- `.env.local` takes precedence over `.env.development` and `.env.production`
- Never commit `.env.local` to version control (add it to `.gitignore`)

## API Endpoint Configuration

### Base API Configuration

Create an API configuration file (`src/config/api.js` or `src/config/api.ts`):

```javascript
// src/config/api.js

const API_CONFIG = {
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001/api',
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
};

// WebSocket configuration
export const WS_CONFIG = {
  url: process.env.REACT_APP_WS_URL || 'ws://localhost:3001',
  reconnectInterval: 3000,
  maxReconnectAttempts: 5,
};

export default API_CONFIG;
```

### Using Axios for HTTP Requests

```javascript
// src/services/api.js
import axios from 'axios';
import API_CONFIG from '../config/api';

const apiClient = axios.create({
  baseURL: API_CONFIG.baseURL,
  timeout: API_CONFIG.timeout,
  headers: API_CONFIG.headers,
});

// Request interceptor for adding auth tokens
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### Using Fetch API

```javascript
// src/services/api.js
import API_CONFIG from '../config/api';

const getAuthHeaders = () => {
  const token = localStorage.getItem('authToken');
  return {
    'Content-Type': 'application/json',
    ...(token && { Authorization: `Bearer ${token}` }),
  };
};

export const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.baseURL}${endpoint}`;
  
  const response = await fetch(url, {
    ...options,
    headers: {
      ...getAuthHeaders(),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`);
  }

  return response.json();
};
```

## Development Setup

### 1. Install Dependencies

```bash
npm install axios
# or
yarn add axios
```

### 2. Configure Proxy (for CORS issues in development)

Add to `package.json`:

```json
{
  "name": "your-react-app",
  "version": "0.1.0",
  "proxy": "http://localhost:3001"
}
```

**Alternative:** Use `setupProxy.js` for more control:

```javascript
// src/setupProxy.js
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:3001',
      changeOrigin: true,
      pathRewrite: {
        '^/api': '', // remove /api prefix when forwarding
      },
    })
  );
};
```

### 3. Example Component Usage

```javascript
// src/components/ExampleComponent.js
import React, { useState, useEffect } from 'react';
import apiClient from '../services/api';

const ExampleComponent = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/endpoint');
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{JSON.stringify(data)}</div>;
};

export default ExampleComponent;
```

## Production Configuration

### Build-Time Environment Variables

React.js embeds environment variables at build time. To use different endpoints for production:

1. Set environment variables before building:
   ```bash
   # Linux/Mac
   REACT_APP_API_BASE_URL=https://api.production.com/api npm run build
   
   # Windows PowerShell
   $env:REACT_APP_API_BASE_URL="https://api.production.com/api"; npm run build
   
   # Windows CMD
   set REACT_APP_API_BASE_URL=https://api.production.com/api && npm run build
   ```

2. Or use `.env.production` file (recommended)

### Runtime Configuration (Advanced)

For runtime endpoint configuration, serve a config file:

```javascript
// public/config.js (served as static file)
window.APP_CONFIG = {
  API_BASE_URL: 'https://api.yourdomain.com/api',
  WS_URL: 'wss://api.yourdomain.com',
};
```

```javascript
// src/config/runtime.js
const getRuntimeConfig = () => {
  // Check for runtime config (production)
  if (window.APP_CONFIG) {
    return window.APP_CONFIG;
  }
  
  // Fall back to build-time env vars (development)
  return {
    API_BASE_URL: process.env.REACT_APP_API_BASE_URL,
    WS_URL: process.env.REACT_APP_WS_URL,
  };
};

export default getRuntimeConfig();
```

## Example Implementation

### Complete API Service Example

```javascript
// src/services/apiService.js
import apiClient from './api';

export const apiService = {
  // GET request
  get: async (endpoint) => {
    const response = await apiClient.get(endpoint);
    return response.data;
  },

  // POST request
  post: async (endpoint, data) => {
    const response = await apiClient.post(endpoint, data);
    return response.data;
  },

  // PUT request
  put: async (endpoint, data) => {
    const response = await apiClient.put(endpoint, data);
    return response.data;
  },

  // DELETE request
  delete: async (endpoint) => {
    const response = await apiClient.delete(endpoint);
    return response.data;
  },
};
```

### WebSocket Connection Example

```javascript
// src/services/websocketService.js
import { WS_CONFIG } from '../config/api';

class WebSocketService {
  constructor() {
    this.ws = null;
    this.reconnectAttempts = 0;
    this.listeners = new Map();
  }

  connect() {
    this.ws = new WebSocket(WS_CONFIG.url);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.emit('message', data);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.attemptReconnect();
    };
  }

  attemptReconnect() {
    if (this.reconnectAttempts < WS_CONFIG.maxReconnectAttempts) {
      this.reconnectAttempts++;
      setTimeout(() => {
        console.log(`Reconnecting... (${this.reconnectAttempts}/${WS_CONFIG.maxReconnectAttempts})`);
        this.connect();
      }, WS_CONFIG.reconnectInterval);
    }
  }

  on(event, callback) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, []);
    }
    this.listeners.get(event).push(callback);
  }

  emit(event, data) {
    if (this.listeners.has(event)) {
      this.listeners.get(event).forEach(callback => callback(data));
    }
  }

  send(data) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export default new WebSocketService();
```

## Common Endpoint Patterns

### RESTful API Endpoints

```javascript
// Example endpoint structure
const endpoints = {
  // Authentication
  login: '/auth/login',
  logout: '/auth/logout',
  register: '/auth/register',
  
  // User management
  getUser: (id) => `/users/${id}`,
  updateUser: (id) => `/users/${id}`,
  deleteUser: (id) => `/users/${id}`,
  
  // Resource endpoints
  getResources: '/resources',
  getResource: (id) => `/resources/${id}`,
  createResource: '/resources',
  updateResource: (id) => `/resources/${id}`,
  deleteResource: (id) => `/resources/${id}`,
};
```

## Troubleshooting

### CORS Issues

If you encounter CORS errors:
1. Configure proxy in `package.json` (development)
2. Ensure backend has proper CORS headers
3. Use environment variables for different origins

### Environment Variables Not Working

- Ensure variables are prefixed with `REACT_APP_`
- Restart development server after adding new variables
- Check `.env` file is in project root
- Verify `.env` files are not in `.gitignore` (except `.env.local`)

### Connection Refused

- Verify backend server is running
- Check endpoint URL matches backend port
- Ensure firewall/network allows connections

## Security Best Practices

1. **Never expose sensitive keys** in client-side code
2. **Use HTTPS** in production
3. **Validate and sanitize** all API responses
4. **Implement proper authentication** (JWT tokens, etc.)
5. **Use environment variables** for configuration
6. **Enable CORS** only for trusted domains

## Additional Resources

- [React Environment Variables](https://create-react-app.dev/docs/adding-custom-environment-variables/)
- [Axios Documentation](https://axios-http.com/docs/intro)
- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)

