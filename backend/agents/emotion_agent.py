import json
from typing import Any

from agents.llm_client import chat_json


def _fallback_emotion(player_input: str) -> dict[str, int]:
    text = player_input.lower()
    threat_words = ["kill", "die", "give me", "shut up", "威胁", "死", "钥匙给我"]
    help_words = ["save", "help", "trust", "protect", "rescue", "救", "帮", "保护"]
    if any(word in text for word in threat_words):
        return {"fear": 10, "trust": -20, "anger": 15}
    if any(word in text for word in help_words):
        return {"fear": -10, "trust": 15, "anger": 0}
    return {"fear": -2, "trust": 3, "anger": 0}


def run_emotion_agent(state: dict[str, Any]) -> dict[str, Any]:
    npc_state = state["npc_state"]
    player_input = state["player_input"]
    fallback = {
        "emotion_update": _fallback_emotion(player_input),
        "reasoning_summary": "Used keyword-based fallback emotion analysis.",
    }
    result = chat_json(
        "You are an Emotion Agent for a game NPC. Return only JSON.",
        f"""
NPC state:
{json.dumps(npc_state, ensure_ascii=False)}

Player input:
{player_input}

Analyze intent and return:
{{
  "emotion_update": {{"fear": integer -30..30, "trust": integer -30..30, "anger": integer -30..30}},
  "reasoning_summary": "short summary"
}}
""",
        fallback,
    )
    update = result.get("emotion_update", fallback["emotion_update"])
    update = {
        "fear": max(-30, min(30, int(update.get("fear", 0)))),
        "trust": max(-30, min(30, int(update.get("trust", 0)))),
        "anger": max(-30, min(30, int(update.get("anger", 0)))),
    }
    state["emotion_update"] = update
    state["agent_log"].append(
        {
            "agent": "Emotion Agent",
            "reasoning_summary": result.get("reasoning_summary", "Updated NPC emotion values."),
            "output": update,
        }
    )
    return state
