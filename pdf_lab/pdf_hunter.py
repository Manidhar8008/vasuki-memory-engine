from pypdf import PdfReader
import os

pdf_path = input("PDF path: ")

reader = PdfReader(pdf_path)

text = ""

for page in reader.pages:
    text += page.extract_text() or ""

name = os.path.basename(pdf_path)
txt_name = name.replace(".pdf", ".txt")

with open(txt_name, "w", encoding="utf-8") as f:
    f.write(text)

print(f"\nSaved: {txt_name}")
print(f"Characters: {len(text)}")
