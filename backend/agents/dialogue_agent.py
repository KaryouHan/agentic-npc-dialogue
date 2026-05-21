import json
from typing import Any

from agents.llm_client import chat_json
from npc_state import NPC_PROFILE


def _fallback_reply(action: str) -> str:
    replies = {
        "hesitate": "……近づかないで。あなたが追っ手じゃないって、まだ信じられない。",
        "ask_identity": "本当に助けに来たなら……まず、あなたの名前を教えて。",
        "refuse": "いや……怖がらせる人に、この鍵は渡せない。",
        "give_key": "これを持って。地下通路を開ける鍵よ……お願い、信じさせて。",
        "follow_player": "分かった……あなたについて行く。でも足音が聞こえたら、すぐ走るから。",
        "reveal_secret": "旧儀式堂の下に、地下通路があるの。鍵は私が持ってる……だから追われてる。",
        "start_escape_quest": "……少しだけ、信じてみる。地下通路まで、私を連れて行って。",
        "end_dialogue": "もう話してる時間はない……追っ手が近い。",
    }
    return replies.get(action, replies["hesitate"])


def run_dialogue_agent(state: dict[str, Any]) -> dict[str, Any]:
    fallback = {
        "reply": _fallback_reply(state["action"]),
        "memory_update": state["memory_update"],
        "reasoning_summary": "Generated fallback dialogue from the selected action.",
    }
    result = chat_json(
        "You are a Dialogue Agent for a cinematic game NPC. Return only JSON.",
        f"""
NPC profile:
{NPC_PROFILE}

Current/projected state:
{json.dumps(state["projected_state"], ensure_ascii=False)}

Quest update: {state["quest_update"]}
Action: {state["action"]}
Recent memory:
{json.dumps(state["memories"], ensure_ascii=False)}
Recent dialogue:
{json.dumps(state["history"], ensure_ascii=False)}
Player input:
{state["player_input"]}

Write a short in-character NPC reply in Japanese. アリス is scared and guarded. Do not expose hidden chain-of-thought.
Return:
{{
  "reply": "Japanese NPC dialogue",
  "memory_update": "one concise persistent memory about this turn",
  "reasoning_summary": "short visible summary of why this line fits"
}}
""",
        fallback,
        temperature=0.7,
    )
    state["reply"] = str(result.get("reply", fallback["reply"]))[:1000]
    state["memory_update"] = str(result.get("memory_update", fallback["memory_update"]))[:500]
    state["agent_log"].append(
        {
            "agent": "Dialogue Agent",
            "reasoning_summary": result.get("reasoning_summary", "Generated アリス's reply."),
            "output": {
                "reply": state["reply"],
                "memory_update": state["memory_update"],
            },
        }
    )
    return state
