from typing import Any


def run_quest_agent(state: dict[str, Any]) -> dict[str, Any]:
    npc_state = state["projected_state"]
    action = state["action"]
    quest_state = npc_state["quest_state"]
    has_key = npc_state["has_key"]
    relationship = npc_state["relationship"]

    if action == "start_escape_quest" and quest_state == "not_started":
        quest_state = "started"
        relationship = "ally"
    elif action == "give_key" and quest_state in {"not_started", "started"}:
        quest_state = "key_given"
        has_key = False
        relationship = "trusted_ally"
    elif action == "follow_player" and quest_state in {"started", "key_given"}:
        quest_state = "escaped"
    elif action == "refuse" and npc_state["trust"] <= 5 and npc_state["anger"] >= 70:
        quest_state = "failed"

    state["quest_update"] = quest_state
    state["next_has_key"] = has_key
    state["next_relationship"] = relationship
    state["agent_log"].append(
        {
            "agent": "Quest Agent",
            "reasoning_summary": "Updated quest progression from the selected action and projected state.",
            "output": {
                "quest_state": quest_state,
                "has_key": has_key,
                "relationship": relationship,
            },
        }
    )
    return state
