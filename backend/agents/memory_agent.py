from typing import Any

from database import get_recent_history, get_recent_memories


def run_memory_agent(state: dict[str, Any]) -> dict[str, Any]:
    history = get_recent_history()
    memories = get_recent_memories()
    player_input = state["player_input"]
    memory_update = f"Player said: {player_input[:180]}"

    state["history"] = history
    state["memories"] = memories
    state["memory_update"] = memory_update
    state["agent_log"].append(
        {
            "agent": "Memory Agent",
            "reasoning_summary": "Retrieved recent conversation turns and persistent memory from SQLite.",
            "output": {
                "recent_history_count": len(history),
                "memories": memories,
                "memory_update": memory_update,
            },
        }
    )
    return state
