from __future__ import annotations

"""Simple wrapper for the OpenAI ChatGPT API."""

from typing import Any, Dict, List

try:
    import openai
except Exception:  # pragma: no cover - openai may not be installed
    openai = None  # type: ignore


class ChatGPTClient:
    """Interact with OpenAI's ChatGPT API."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo") -> None:
        if openai is None:
            raise ImportError("openai package is required to use ChatGPTClient")
        openai.api_key = api_key
        self.model = model

    def complete(self, prompt: str, *, temperature: float = 0.0, **kwargs: Any) -> str:
        """Return the ChatGPT completion for ``prompt``."""
        messages: List[Dict[str, str]] = [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=self.model, messages=messages, temperature=temperature, **kwargs
        )
        return response.choices[0].message["content"]
