from typing import Any, Literal

from pydantic import BaseModel, Field


QuestState = Literal["not_started", "started", "key_given", "escaped", "failed"]
NpcAction = Literal[
    "hesitate",
    "ask_identity",
    "refuse",
    "give_key",
    "follow_player",
    "reveal_secret",
    "start_escape_quest",
    "end_dialogue",
]


class DialogueRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


class EmotionUpdate(BaseModel):
    fear: int = Field(..., ge=-30, le=30)
    trust: int = Field(..., ge=-30, le=30)
    anger: int = Field(..., ge=-30, le=30)


class NpcState(BaseModel):
    name: str
    fear: int = Field(..., ge=0, le=100)
    trust: int = Field(..., ge=0, le=100)
    anger: int = Field(..., ge=0, le=100)
    quest_state: QuestState
    has_key: bool
    relationship: str


class AgentLogEntry(BaseModel):
    agent: str
    reasoning_summary: str
    output: dict[str, Any]


class DialogueResponse(BaseModel):
    reply: str
    emotion_update: EmotionUpdate
    current_state: NpcState
    action: NpcAction
    quest_update: QuestState
    memory_update: str
    agent_log: list[AgentLogEntry]


class AppStateResponse(BaseModel):
    current_state: NpcState
    history: list[dict[str, str]]
    memories: list[str]
