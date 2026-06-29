import sqlite3
import os
import subprocess
from datetime import datetime

DB = "vasuki.db"

print("DB:", os.path.abspath(DB))

conn = sqlite3.connect(DB)
cur = conn.cursor()

folder = "/storage/emulated/0/Pictures/Screenshots"

count = 0

for root, dirs, files in os.walk(folder):

    for file in files:

        if not file.lower().endswith(
            (".png", ".jpg", ".jpeg")
        ):
            continue

        path = os.path.join(root, file)

        txtfile = "temp_ocr"

        try:

            subprocess.run(
                ["tesseract", path, txtfile],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            with open(
                txtfile + ".txt",
                "r",
                encoding="utf8",
                errors="ignore"
            ) as f:

                text = f.read()

            print("TEXT LENGTH:", len(text))

            cur.execute("""
            INSERT INTO screenshots
            (path, extracted_text, chars, created_at)
            VALUES (?, ?, ?, ?)
            """, (
                path,
                text,
                len(text),
                datetime.now().isoformat()
            ))

            conn.commit()

            count += 1

            print("Indexed:", file)

            if count >= 5:
                break

        except Exception as e:

            print("ERROR:", e)

    if count >= 5:
        break

conn.close()

print("DONE")
