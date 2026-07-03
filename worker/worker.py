import os
import subprocess
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

MODEL = os.getenv(
    "MODEL",
    "meta/llama-3.3-70b-instruct"
)

SYSTEM = """
You are Vasuki Engineering Worker.

Rules:
- Analyze repository structure.
- Suggest precise edits.
- Output executable code.
- Prefer modifying existing files.
- Explain reasoning briefly.
"""

def ask(task):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":SYSTEM},
            {"role":"user","content":task}
        ],
        temperature=0.2,
        max_tokens=2000
    )

    print(
        response.choices[0].message.content
    )

while True:

    cmd = input("\nVASUKI> ")

    if cmd.lower() in ["exit","quit"]:
        break

    ask(cmd)

