import sqlite3

DB="founder.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

cur.execute("""
SELECT filename
FROM founder_core_files
""")

files=[x[0].lower() for x in cur.fetchall()]

targets=[
    "vasuki",
    "mw.ai",
    "janani"
]

print("\nDOCTOR AGENT\n")

for target in targets:

    score=0

    evidence=[]

    for f in files:

        if target in f:

            score+=10
            evidence.append(f)

    print("\n----------------")
    print(target.upper())
    print("----------------")

    print("Energy:",score)

    print("Evidence Count:",len(evidence))

    for e in evidence[:5]:
        print("-",e)

conn.close()
