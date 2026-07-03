import os
from pathlib import Path

ROOT = Path.home() / "vasuki"

def find(text):
    for path in ROOT.rglob("*"):
        if path.is_file():
            try:
                content = path.read_text(errors="ignore")
                if text.lower() in content.lower():
                    print(path)
            except:
                pass

def replace(old, new):
    count = 0

    for path in ROOT.rglob("*"):
        if path.is_file():
            try:
                content = path.read_text(errors="ignore")

                if old in content:
                    content = content.replace(old, new)

                    path.write_text(content)

                    count += 1

                    print("updated", path)

            except:
                pass

    print(f"updated {count} files")


while True:

    cmd = input("worker> ")

    if cmd.startswith("find "):
        find(cmd[5:])

    elif cmd.startswith("replace "):
        parts = cmd.split("|")

        replace(
            parts[1],
            parts[2]
        )

    elif cmd == "quit":
        break
