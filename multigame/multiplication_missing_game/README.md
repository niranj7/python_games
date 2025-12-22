# Multiplication Missing Game

This repository contains a small multiplication missing-number game. The project includes a Python backend and a simple UI layer.

## React.js connection endpoint configuration

When integrating a React frontend with this project, configure the backend connection endpoint via environment variables so the same build can be used across environments.

- Development (Create React App): set variables with the REACT_APP_ prefix in a .env file at the React project root. Example:

```
# .env.development
REACT_APP_BACKEND_URL=http://localhost:8000
REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws
```

- Vite or other bundlers: use the bundler-specific prefix (for Vite use VITE_), e.g. VITE_BACKEND_URL.

Usage examples in React code:

```
const API_BASE = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WEBSOCKET_URL || `ws://${window.location.host}/ws`;

// REST request
fetch(`${API_BASE}/api/game`, { method: 'GET' })

// WebSocket
const socket = new WebSocket(WS_URL);
```

Notes:

- Environment variables must be provided at build time for production builds. For Create React App, prefix variables with REACT_APP_.
- Use ws:// for local development and wss:// for secure deployments behind TLS.
- If your backend exposes a specific socket path (for example /ws), ensure the React WEBSOCKET_URL includes that path.

See the React app's README or config files for exact variable names used there and adapt the examples above accordingly.
