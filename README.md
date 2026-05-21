# Agentic AI NPC Dialogue System

Agent-based AI NPC dialogue demo for a game scenario: the player meets アリス, a hunted magical girl NPC, inside an abandoned magic academy. アリス owns a key to an underground escape route, but she begins scared and distrustful. The player must earn her trust through free-form dialogue to start the escape quest.

## Tech Stack

- Backend: FastAPI
- Agent workflow: LangGraph
- LLM: DeepSeek API, OpenAI-compatible client
- Database: SQLite
- Frontend: React + Vite

## Features

- Free-form player input
- Persistent NPC state: fear, trust, anger, quest state, relationship, key ownership
- Agent pipeline: Memory, Emotion, Action, Quest, Dialogue, State Update
- Structured JSON responses
- SQLite conversation history and NPC memory
- Game-style UI with NPC status, chat, and agent decision log
- Reset demo button

## Project Structure

```text
agentic-npc-dialogue/
├── backend/
│   ├── agents/
│   ├── database.py
│   ├── graph.py
│   ├── main.py
│   ├── npc_state.py
│   ├── requirements.txt
│   └── schemas.py
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── docker-compose.yml
└── README.md
```

## Setup

### 1. Configure environment

Copy `.env.example` to `.env` and set your DeepSeek API key:

```bash
cp .env.example .env
```

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
DATABASE_URL=sqlite:///./npc_memory.db
FRONTEND_ORIGIN=http://localhost:5173
VITE_API_BASE=http://127.0.0.1:8000
```

### 2. Run backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Run frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, usually `http://localhost:5173`.

If the project folder is moved, recreate the backend virtual environment because `.venv` contains absolute paths:

```bash
cd backend
python -m venv --clear .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API

### `GET /api/state`

Returns current NPC state and recent dialogue history.

### `POST /api/dialogue`

Request:

```json
{
  "message": "私はあなたを助けに来た。"
}
```

Response:

```json
{
  "reply": "……助けに来たの？ なら、どうして信じていいのか教えて。",
  "emotion_update": {
    "fear": -5,
    "trust": 10,
    "anger": 0
  },
  "current_state": {
    "name": "アリス",
    "fear": 75,
    "trust": 30,
    "anger": 10,
    "quest_state": "not_started",
    "has_key": true,
    "relationship": "stranger"
  },
  "action": "ask_identity",
  "quest_update": "not_started",
  "memory_update": "The player said they came to save アリス.",
  "agent_log": []
}
```

### `POST /api/reset`

Resets the demo state and clears memory/history.

## Resume Bullet

LLM Agentを用いて、NPCの感情状態・記憶・クエスト進行・行動選択を統合的に管理するゲームNPC対話システムを開発。FastAPI、LangGraph、SQLite、Reactを用いて、プレイヤー入力に応じた自然な会話生成と状態遷移を実現した。
