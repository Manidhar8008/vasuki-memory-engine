from pathlib import Path
import sqlite3
import pytesseract
from PIL import Image

DB = "vasuki.db"

SCAN_DIRS = [
    "/storage/emulated/0/Pictures/Screenshots",
    "/storage/emulated/0/DCIM",
    "/storage/emulated/0/Download"
]

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS ocr_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_path TEXT UNIQUE,
    raw_text TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

count = 0

for folder in SCAN_DIRS:

    p = Path(folder)

    if not p.exists():
        continue

    for img in p.rglob("*"):

        if img.suffix.lower() not in [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        ]:
            continue

        try:

            cur.execute(
                "SELECT 1 FROM ocr_records WHERE file_path=?",
                (str(img),)
            )

            if cur.fetchone():
                continue

            text = pytesseract.image_to_string(
                Image.open(img)
            ).strip()

            if not text:
                continue

            cur.execute(
                """
                INSERT INTO ocr_records(
                    file_path,
                    raw_text
                )
                VALUES (?,?)
                """,
                (
                    str(img),
                    text[:50000]
                )
            )

            conn.commit()

            count += 1

            print(
                f"[OCR] {count} | {img.name}"
            )

        except Exception as e:

            print(
                f"[ERR] {img.name} | {e}"
            )

print()
print("="*60)
print("OCR COMPLETE")
print("NEW RECORDS:", count)
print("="*60)

conn.close()
