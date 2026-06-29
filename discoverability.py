from pathlib import Path
from collections import Counter

root = Path.home() / "vasuki"

files = list(root.rglob("*"))

py_files = []
db_files = []
md_files = []
sql_files = []

for f in files:
    if not f.is_file():
        continue

    suffix = f.suffix.lower()

    if suffix == ".py":
        py_files.append(f)

    elif suffix == ".db":
        db_files.append(f)

    elif suffix == ".md":
        md_files.append(f)

    elif suffix == ".sql":
        sql_files.append(f)

print("=" * 60)
print("VASUKI DISCOVERY REPORT")
print("=" * 60)

print(f"Python Files : {len(py_files)}")
print(f"Databases    : {len(db_files)}")
print(f"Markdown     : {len(md_files)}")
print(f"SQL Files    : {len(sql_files)}")

print("\nDATABASES")
for db in db_files:
    print("-", db)

print("\nTOP LEVEL PYTHON FILES")
for py in sorted(py_files)[:50]:
    print("-", py.name)
