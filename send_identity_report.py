import sqlite3
import requests

BOT_TOKEN = "YOUR_BOT_TOKEN"

CHAT_ID = "YOUR_CHAT_ID"

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
SELECT
title,
COUNT(*)
FROM timeline
GROUP BY title
ORDER BY COUNT(*) DESC
LIMIT 20
""")

rows = cur.fetchall()

msg = "VASUKI TIMELINE REPORT\n\n"

for title,count in rows:

    msg += f"{title}: {count}\n"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    json={
        "chat_id": CHAT_ID,
        "text": msg
    }
)

conn.close()

print("Report Sent")

