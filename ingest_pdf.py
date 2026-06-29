import sqlite3
import os
from pypdf import PdfReader

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    path TEXT,
    chars INTEGER,
    content TEXT
)
""")

pdf_path = input("PDF path: ")

reader = PdfReader(pdf_path)

text = ""
for page in reader.pages:
    text += page.extract_text() or ""

cur.execute(
    "INSERT INTO documents(title,path,chars,content) VALUES(?,?,?,?)",
    (
        os.path.basename(pdf_path),
        pdf_path,
        len(text),
        text
    )
)

conn.commit()

print("Saved to database!")
print("Characters:", len(text))

conn.close()
