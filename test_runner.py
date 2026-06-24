import os

scripts = [
    "ask_vasuki.py",
    "ask_vasuki_v3.py",
    "ask_founder.py",
    "classify_memories.py",
    "founder_dashboard.py",
]

print("\n=== VASUKI HEALTH CHECK ===\n")

for script in scripts:

    if os.path.exists(script):
        print(f"[OK] {script}")
    else:
        print(f"[MISSING] {script}")
