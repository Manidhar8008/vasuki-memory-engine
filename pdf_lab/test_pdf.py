from pypdf import PdfReader

pdf_path = input("Enter PDF path: ")

reader = PdfReader(pdf_path)

print(f"Pages: {len(reader.pages)}")

text = ""

for page in reader.pages[:5]:
    text += page.extract_text() or ""

print(text[:2000])

