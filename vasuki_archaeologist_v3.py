import os
import sqlite3
import fitz
import pytesseract
from PIL import Image
from datetime import datetime

# =========================
# CONFIG
# =========================

DB = "vasuki.db"
ROOT = "/storage/emulated/0"

# =========================
# DATABASE
# =========================

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS artifacts_v2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    original_path TEXT UNIQUE,
    original_name TEXT,

    generated_title TEXT,
    suggested_filename TEXT,

    file_type TEXT,
    project TEXT,

    extracted_text TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================
# PROJECT RULES
# =========================

PROJECT_RULES = {
    "vasuki": "Vasuki",
    "janani": "Janani",
    "startup": "Startup",
    "founder": "Startup",
    "palantir": "Career",
    "resume": "Career",
    "offer letter": "Career",
    "interview": "Career",
    "python": "Engineering",
    "sql": "Engineering",
    "database": "Engineering",
    "machine learning": "AI",
    "artificial intelligence": "AI",
    "agent": "AI",
    "llm": "AI",
}

# =========================
# HELPERS
# =========================

def clean_filename(text):
    bad = '\\/:*?"<>|'

    for ch in bad:
        text = text.replace(ch, "")

    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    words = text.split()

    return "_".join(words[:12])


def generate_title(text):

    lines = text.splitlines()

    for line in lines[:30]:

        line = line.strip()

        if len(line) > 15:
            return line[:120]

    return "Unknown Document"


def detect_project(text):

    txt = text.lower()

    for keyword, project in PROJECT_RULES.items():

        if keyword in txt:
            return project

    return "Unclassified"


# =========================
# PDF EXTRACTION
# =========================

def extract_pdf(path):

    try:

        doc = fitz.open(path)

        text = ""

        for page in doc:
            text += page.get_text()

        return text

    except Exception as e:

        print(f"[PDF ERROR] {path}")
        print(e)

        return ""


# =========================
# IMAGE OCR
# =========================

def extract_image(path):

    try:

        img = Image.open(path)

        text = pytesseract.image_to_string(img)

        return text

    except Exception as e:

        print(f"[IMG ERROR] {path}")
        print(e)

        return ""


# =========================
# TEXT FILE
# =========================

def extract_text(path):

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            return f.read()

    except:

        return ""


# =========================
# SAVE
# =========================

def save_record(
    path,
    title,
    suggestion,
    file_type,
    project,
    text
):

    try:

        cur.execute("""
        INSERT OR REPLACE INTO artifacts_v2
        (
            original_path,
            original_name,
            generated_title,
            suggested_filename,
            file_type,
            project,
            extracted_text
        )
        VALUES
        (
            ?,?,?,?,?,?,?
        )
        """,
        (
            path,
            os.path.basename(path),
            title,
            suggestion,
            file_type,
            project,
            text[:5000]
        ))

        conn.commit()

    except Exception as e:

        print("[DB ERROR]")
        print(e)


# =========================
# PROCESS FILE
# =========================

def process_file(path):

    ext = path.lower()

    text = ""

    if ext.endswith(".pdf"):
        text = extract_pdf(path)

    elif ext.endswith((".png", ".jpg", ".jpeg")):
        text = extract_image(path)

    elif ext.endswith((".txt", ".md")):
        text = extract_text(path)

    else:
        return

    if len(text.strip()) < 50:
        return

    title = generate_title(text)

    project = detect_project(text)

    suggestion = clean_filename(title)

    save_record(
        path,
        title,
        suggestion,
        os.path.splitext(path)[1],
        project,
        text
    )

    print(
        f"[{project}] "
        f"{os.path.basename(path)} "
        f"-> "
        f"{suggestion}"
    )


# =========================
# MAIN
# =========================

print("\n=================================")
print("VASUKI ARCHAEOLOGIST V3")
print("=================================")
print("Scanning:", ROOT)
print("Started :", datetime.now())
print("=================================\n")

count = 0

for root, dirs, files in os.walk(ROOT):

    for file in files:

        path = os.path.join(root, file)

        try:

            process_file(path)

            count += 1

            if count % 100 == 0:
                print(f"\nProcessed {count} files\n")

        except Exception as e:

            print("[ERROR]")
            print(path)
            print(e)

print("\n=================================")
print("SCAN COMPLETE")
print("Files Seen:", count)
print("=================================\n")

conn.close()
