#!/data/data/com.termux/files/usr/bin/bash

mkdir -p providers

echo "Creating providers/nvidia.py..."

cat > providers/nvidia.py << 'EOF'
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
EOF


echo "Creating brain.py..."

cat > brain.py << 'EOF'
from providers.nvidia import ask_nvidia
from memory import search


def think(question):

    memories = search(question)

    if memories:

        context = "\n".join(
            x["content"]
            for x in memories
        )

        return f"Memory:\n\n{context}"

    return ask_nvidia(question)
EOF


echo "Creating router.py..."

cat > router.py << 'EOF'
from memory import save_memory
from memory import recent
from brain import think


def handle(command):

    text = command.strip()

    if text.startswith("remember"):

        content = text.replace("remember","",1).strip()

        save_memory(content)

        return "✓ Memory stored."

    if text == "recent":

        rows = recent()

        if not rows:
            return "No memories."

        return "\n".join(
            f"- {x['content']}"
            for x in rows
        )

    if text.startswith("ask"):

        q = text.replace("ask","",1).strip()

        return think(q)

    if text == "status":

        return """
VASUKI STATUS

Kernel  ✅

Memory  ✅

Brain   ✅

Ready.
"""

    if text == "help":

        return """
remember <text>

recent

ask <question>

status

exit
"""

    return "Unknown command."
EOF


echo "Creating main.py..."

cat > main.py << 'EOF'
from router import handle

print()

print("VASUKI OS")

print()

while True:

    cmd = input("🎤 Vasuki > ")

    if cmd.lower() == "exit":
        break

    print()

    print(handle(cmd))

    print()
EOF

echo ""
echo "STEP 2 COMPLETE"
echo ""
echo "Run:"
echo "python main.py"
