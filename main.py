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
