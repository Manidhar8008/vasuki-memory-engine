quality = 0

if len(memory) > 100:
    quality += 1

if "vasuki" in text:
    quality += 2

if "janani" in text:
    quality += 2

if "decision" in text:
    quality += 2

if "learned" in text:
    quality += 2

if "goal" in text:
    quality += 2
