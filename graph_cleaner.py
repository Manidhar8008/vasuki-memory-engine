import sqlite3

STOPWORDS = {
    "under","section","terms","conditions",
    "account","number","date","birth",
    "shall","only","same","used",
    "hereinafter","referred"
}

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

for word in STOPWORDS:

    cur.execute(
        "DELETE FROM graph WHERE source=? OR target=?",
        (word, word)
    )

conn.commit()

print("GRAPH CLEANED")

conn.close()


