import os
import re
from PIL import Image
import pytesseract

ROOT = "/storage/emulated/0/Pictures"

DRY_RUN = True

def clean_name(text):

    text = text.strip()

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    words = text.split()

    if not words:
        return None

    return "_".join(words[:8])


def extract_title(path):

    try:

        text = pytesseract.image_to_string(
            Image.open(path)
        )

        lines = [
            x.strip()
            for x in text.split("\n")
            if len(x.strip()) > 8
        ]

        if lines:
            return clean_name(lines[0])

    except:
        pass

    return None


for root, dirs, files in os.walk(ROOT):

    for file in files:

        if not file.lower().endswith(
            (".png",".jpg",".jpeg")
        ):
            continue

        path = os.path.join(root,file)

        title = extract_title(path)

        if not title:
            continue

        ext = os.path.splitext(file)[1]

        new_name = f"{title}{ext}"

        new_path = os.path.join(
            root,
            new_name
        )

        print(
            f"{file} -> {new_name}"
        )

        if not DRY_RUN:

            try:
                os.rename(
                    path,
                    new_path
                )
            except:
                pass
