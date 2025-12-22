# Balloon Pop (Pygame)

A small balloon pop demo built with Pygame. The project separates game logic and UI rendering for clarity and learning.

## Requirements

- Python 3.8+ (Windows tested)
- pygame

Install dependencies:

```bash
pip install pygame
```

## Run

From the project root run:

```bash
python main.py
```

## Controls

- Use the mouse to interact with the game (click to pop balloons).

## Project structure

- main.py — entry point that starts the game loop
- logic/ — game logic modules (e.g. `game_logic.py`)
- ui/ — rendering and UI helpers (e.g. `ui_render.py`)

## React.js connection endpoint

If you have a React.js frontend that connects to this project (for example to receive game state or send input), configure the connection endpoint used by the frontend:

- **Default endpoint:** `http://localhost:5000` (HTTP) or `ws://localhost:5000` (WebSocket) — change as needed.
- **How to configure:** set the endpoint in your React app using an environment variable (for example, `REACT_APP_GAME_ENDPOINT`) or in a configuration file.

Example `.env` for a Create React App project:

```bash
REACT_APP_GAME_ENDPOINT=http://localhost:5000
REACT_APP_GAME_WS=ws://localhost:5000
```

Usage example in React:

```js
const apiUrl = process.env.REACT_APP_GAME_ENDPOINT || 'http://localhost:5000';
const wsUrl = process.env.REACT_APP_GAME_WS || 'ws://localhost:5000';
// fetch(`${apiUrl}/score`)
// const socket = new WebSocket(wsUrl);
```

Notes:

- Ensure any backend server used by React (HTTP or WebSocket) is running and accessible.
- If running cross-origin (different host/port), enable CORS on the server and update the endpoint accordingly.

## Notes

- This is a small educational project. Look in `logic/game_logic.py` and `ui/ui_render.py` to explore the code split between logic and rendering.

## Contributing

Small fixes and improvements welcome — open an issue or submit a PR.

## License

MIT — feel free to reuse and modify.
