import json
from typing import Any

from agents.llm_client import chat_json


VALID_ACTIONS = {
    "hesitate",
    "ask_identity",
    "refuse",
    "give_key",
    "follow_player",
    "reveal_secret",
    "start_escape_quest",
    "end_dialogue",
}


def _projected_state(npc_state: dict[str, Any], emotion_update: dict[str, int]) -> dict[str, Any]:
    projected = dict(npc_state)
    for key in ("fear", "trust", "anger"):
        projected[key] = max(0, min(100, int(projected[key]) + int(emotion_update.get(key, 0))))
    return projected


def _fallback_action(projected: dict[str, Any]) -> str:
    if projected["anger"] >= 70 or projected["trust"] <= 5:
        return "refuse"
    if projected["trust"] >= 65 and projected["fear"] <= 65 and projected["quest_state"] == "not_started":
        return "start_escape_quest"
    if projected["trust"] >= 75 and projected["has_key"]:
        return "give_key"
    if projected["trust"] >= 45:
        return "reveal_secret"
    if projected["trust"] >= 30:
        return "ask_identity"
    return "hesitate"


def run_action_agent(state: dict[str, Any]) -> dict[str, Any]:
    projected = _projected_state(state["npc_state"], state["emotion_update"])
    fallback_action = _fallback_action(projected)
    fallback = {
        "action": fallback_action,
        "reasoning_summary": "Selected action with deterministic fallback thresholds.",
    }
    result = chat_json(
        "You are an Action Agent for a game NPC. Return only JSON.",
        f"""
Projected NPC state after emotion update:
{json.dumps(projected, ensure_ascii=False)}

Player input:
{state["player_input"]}

Choose exactly one action:
hesitate, ask_identity, refuse, give_key, follow_player, reveal_secret, start_escape_quest, end_dialogue

Return:
{{"action": "one action", "reasoning_summary": "short summary"}}
""",
        fallback,
    )
    action = result.get("action", fallback_action)
    if action not in VALID_ACTIONS:
        action = fallback_action
    state["projected_state"] = projected
    state["action"] = action
    state["agent_log"].append(
        {
            "agent": "Action Agent",
            "reasoning_summary": result.get("reasoning_summary", "Selected the next NPC action."),
            "output": {"action": action},
        }
    )
    return state
