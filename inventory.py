import os

print("\n=== VASUKI INVENTORY ===\n")

for file in sorted(os.listdir(".")):

    if file.endswith(".py"):
        print(file)
