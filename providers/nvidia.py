import os
import requests

API_KEY = os.getenv("NVIDIA_API_KEY")


def ask_nvidia(prompt):

    if not API_KEY:
        return "NVIDIA_API_KEY not configured."

    url = "https://integrate.api.nvidia.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta/llama-3.1-8b-instruct",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.2,
        "max_tokens": 512
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        return r.text

    return r.json()["choices"][0]["message"]["content"]
