import json
import os
from typing import Any

from openai import OpenAI


def get_client() -> OpenAI:
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not configured.")
    return OpenAI(
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
    )


def chat_json(
    system_prompt: str,
    user_prompt: str,
    fallback: dict[str, Any],
    temperature: float = 0.4,
) -> dict[str, Any]:
    """Call DeepSeek and parse a JSON object. Falls back to deterministic logic on API errors."""
    try:
        completion = get_client().chat.completions.create(
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=temperature,
        )
        content = completion.choices[0].message.content or "{}"
        return json.loads(content)
    except Exception:
        return fallback
