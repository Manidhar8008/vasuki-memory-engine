from pathlib import Path

ROOT = Path.home() / "vasuki"

IGNORE = {
    "venv",
    "node_modules",
    "__pycache__",
    ".git"
}

for p in ROOT.rglob("*.py"):
    if any(part in IGNORE for part in p.parts):
        continue

    print(p.relative_to(ROOT))
