from pathlib import Path

root = "/storage/emulated/0"

count = 0

for file in Path(root).rglob("*"):
    if file.is_file():
        print(file)
        count += 1

print(f"\nFiles Found: {count}")
