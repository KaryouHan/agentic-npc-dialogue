from contextlib import asynccontextmanager
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(BASE_DIR / ".env")

from database import get_recent_history, get_recent_memories, init_db, load_npc_state, reset_demo
from graph import run_dialogue_turn
from schemas import AppStateResponse, DialogueRequest, DialogueResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Agentic AI NPC Dialogue System",
    description="Agent-based NPC dialogue demo with persistent emotion, memory, action, and quest state.",
    version="0.1.0",
    lifespan=lifespan,
)

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/state", response_model=AppStateResponse)
def get_state() -> dict:
    init_db()
    return {
        "current_state": load_npc_state(),
        "history": get_recent_history(),
        "memories": get_recent_memories(),
    }


@app.post("/api/dialogue", response_model=DialogueResponse)
def dialogue(request: DialogueRequest) -> dict:
    init_db()
    return run_dialogue_turn(request.message)


@app.post("/api/reset", response_model=AppStateResponse)
def reset() -> dict:
    init_db()
    reset_demo()
    return {
        "current_state": load_npc_state(),
        "history": get_recent_history(),
        "memories": get_recent_memories(),
    }
