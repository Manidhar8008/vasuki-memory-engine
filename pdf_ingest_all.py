from pathlib import Path
from pypdf import PdfReader
import sqlite3

conn = sqlite3.connect("vasuki.db")
cur = conn.cursor()

pdfs = Path("/storage/emulated/0").rglob("*.pdf")

count = 0

for pdf in pdfs:

    try:

        text = ""

        reader = PdfReader(str(pdf))

        for page in reader.pages:
            text += page.extract_text() or ""

        cur.execute("""
        INSERT INTO documents
        (
            title,
            path,
            content,
            chars
        )
        VALUES (?, ?, ?, ?)
        """, (
            pdf.name,
            str(pdf),
            text,
            len(text)
        ))

        count += 1

        print("Saved:", pdf.name)

    except Exception as e:
        print("Failed:", pdf.name)

conn.commit()
conn.close()

print("\nDONE")
print("PDFs indexed:", count)
