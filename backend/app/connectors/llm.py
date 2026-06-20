import os
import requests

# NVIDIA NIM — OpenAI-compatible chat completions.
NIM_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = os.getenv("LLM_MODEL", "minimaxai/minimax-m3")


def chat(messages: list[dict], max_tokens: int = 1024, temperature: float = 0.4) -> str:
    key = os.environ["NVIDIA_API_KEY"]
    r = requests.post(
        NIM_URL,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.95,
        },
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()
