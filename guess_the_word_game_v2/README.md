# Guess the Word — Intermediate

This repository contains a Pygame desktop game. There is no built-in web API or server in this project.

## Quick start

- Install dependencies: `pip install -r requirements.txt`
- Run the game: `python src/main.py`

## React Integration — Connection Endpoint

This project is a native Pygame application and does not expose an HTTP or WebSocket endpoint by default. If you want to build a React.js frontend that connects to the game, you will need to implement a separate backend (HTTP or WebSocket) that the React app can call.

Recommended configuration and conventions for the React side:

- Environment variable: use `REACT_APP_GAME_ENDPOINT` in your React app to store the backend URL (example: `http://localhost:8000`).
- Create React App: put a `.env` file in your React project with:

  REACT_APP_GAME_ENDPOINT=http://localhost:8000

- Access the value in code via `process.env.REACT_APP_GAME_ENDPOINT`.
- If you prefer a development proxy, add this to `package.json` of the React app:

  "proxy": "http://localhost:8000"

Examples

- Fetch example (HTTP REST API):

```js
const API = process.env.REACT_APP_GAME_ENDPOINT;
# Guess the Word — Intermediate

This repository contains a Pygame desktop game. There is no built-in web API or server in this project.

## Quick start

- Install dependencies: `pip install -r requirements.txt`
- Run the game: `python src/main.py`

## React Integration — Connection Endpoint

This project is a native Pygame application and does not expose an HTTP or WebSocket endpoint by default. If you want to build a React.js frontend that connects to the game, you will need to implement a separate backend (HTTP or WebSocket) that the React app can call.

Recommended configuration and conventions for the React side:

- Environment variable: use `REACT_APP_GAME_ENDPOINT` in your React app to store the backend URL (example: `http://localhost:8000`).
- Create React App: put a `.env` file in your React project with:

  REACT_APP_GAME_ENDPOINT=http://localhost:8000

- Access the value in code via `process.env.REACT_APP_GAME_ENDPOINT`.
- If you prefer a development proxy, add this to `package.json` of the React app:

  "proxy": "http://localhost:8000"

Examples

- Fetch example (HTTP REST API):

```js
const API = process.env.REACT_APP_GAME_ENDPOINT;
fetch(`${API}/state`)
  .then(r => r.json())
  .then(data => console.log(data));
```

- WebSocket example:

```js
const WS = (process.env.REACT_APP_GAME_ENDPOINT || 'ws://localhost:8000').replace(/^http/, 'ws');
const socket = new WebSocket(WS + '/ws');
socket.onmessage = (ev) => console.log('msg', ev.data);
```

Security & deployment

- Use `wss://` and `https://` for production endpoints.
- Set the environment variable on your hosting platform (Netlify, Vercel, etc.) or in CI.

Notes

- Because this repository currently contains only a desktop Pygame app, follow one of these approaches to integrate a React frontend:
  - Implement a lightweight server that exposes the game state and controls (HTTP/WebSocket) and run it alongside the game process.
  - Re-implement the game logic as a web service if you want a fully web-native experience.

If you want, I can add a minimal example backend (Flask or Express) showing how to expose an endpoint for a React app to consume.
