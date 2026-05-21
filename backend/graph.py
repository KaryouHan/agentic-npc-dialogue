from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from agents.action_agent import run_action_agent
from agents.dialogue_agent import run_dialogue_agent
from agents.emotion_agent import run_emotion_agent
from agents.memory_agent import run_memory_agent
from agents.quest_agent import run_quest_agent
from database import add_history, add_memory, load_npc_state, save_npc_state


class WorkflowState(TypedDict, total=False):
    player_input: str
    npc_state: dict[str, Any]
    projected_state: dict[str, Any]
    history: list[dict[str, str]]
    memories: list[str]
    emotion_update: dict[str, int]
    action: str
    quest_update: str
    next_has_key: bool
    next_relationship: str
    reply: str
    memory_update: str
    agent_log: list[dict[str, Any]]
    current_state: dict[str, Any]


def clamp(value: int) -> int:
    return max(0, min(100, int(value)))


def apply_state_update(state: WorkflowState) -> WorkflowState:
    current = dict(state["npc_state"])
    emotion_update = state["emotion_update"]
    for key in ("fear", "trust", "anger"):
        current[key] = clamp(current[key] + emotion_update.get(key, 0))

    current["quest_state"] = state["quest_update"]
    current["has_key"] = state["next_has_key"]
    current["relationship"] = state["next_relationship"]

    add_history("player", state["player_input"])
    add_history("alice", state["reply"])
    add_memory(state["memory_update"])
    save_npc_state(current)

    state["current_state"] = current
    state["agent_log"].append(
        {
            "agent": "State Update",
            "reasoning_summary": "Applied emotion deltas, quest changes, and persisted the turn to SQLite.",
            "output": current,
        }
    )
    return state


def build_graph():
    workflow = StateGraph(WorkflowState)
    workflow.add_node("memory_agent", run_memory_agent)
    workflow.add_node("emotion_agent", run_emotion_agent)
    workflow.add_node("action_agent", run_action_agent)
    workflow.add_node("quest_agent", run_quest_agent)
    workflow.add_node("dialogue_agent", run_dialogue_agent)
    workflow.add_node("state_update", apply_state_update)

    workflow.set_entry_point("memory_agent")
    workflow.add_edge("memory_agent", "emotion_agent")
    workflow.add_edge("emotion_agent", "action_agent")
    workflow.add_edge("action_agent", "quest_agent")
    workflow.add_edge("quest_agent", "dialogue_agent")
    workflow.add_edge("dialogue_agent", "state_update")
    workflow.add_edge("state_update", END)
    return workflow.compile()


NPC_GRAPH = build_graph()


def run_dialogue_turn(player_input: str) -> dict[str, Any]:
    initial_state: WorkflowState = {
        "player_input": player_input,
        "npc_state": load_npc_state(),
        "agent_log": [],
    }
    result = NPC_GRAPH.invoke(initial_state)
    return {
        "reply": result["reply"],
        "emotion_update": result["emotion_update"],
        "current_state": result["current_state"],
        "action": result["action"],
        "quest_update": result["quest_update"],
        "memory_update": result["memory_update"],
        "agent_log": result["agent_log"],
    }
