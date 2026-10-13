# Vasuki Founder OS — local MVP

This is a deliberately small, **local-only, read-only** demo layer over the existing Vasuki SQLite database. It does not replace the existing pipeline, rewrite schemas, or claim that noisy ontology rows are trustworthy.

## Run on Termux

From the repository root:

```sh
python demo/vasuki_demo.py ~/vasuki/vasuki.db
```

Then open **http://127.0.0.1:8765** on the same device. Stop with `Ctrl+C`.

Optional custom port:

```sh
VASUKI_PORT=8766 python demo/vasuki_demo.py ~/vasuki/vasuki.db
```

No pip install is required; the server uses Python's standard library.

## MVP capabilities

- Reads database table/column metadata at runtime, so it tolerates schema variation.
- Displays live counts for tables it finds, including documents, memories, entities, ontology objects, and founder truths.
- Searches selected, known text columns and returns the source table and row ID for each evidence candidate.
- Uses SQLite read-only mode; the app has no database write or file-upload route.
- Binds only to `127.0.0.1`; it is not a network-accessible multi-user service.
- Makes no external API calls.

## Current limitations

- Search is keyword retrieval, **not semantic reasoning**. A result is evidence to inspect, not a verified conclusion.
- It does not extract new text from PDFs or OCR images; it reads content already stored in the database.
- Table-specific search fields are allowlisted in `SAFE_TABLES`. Add a field there only after verifying that the field exists and is safe to display.
- No authentication is included because this is a loopback-only personal demo. Do not bind it to `0.0.0.0`, port-forward it, or expose it through a tunnel.
- The interface is not a security boundary against other processes or people with access to the unlocked device.

## Data handling and safety

The GitHub repository should contain **code and synthetic tests only**. Do not commit the private `vasuki.db`, founder notes, raw documents, OCR dumps, exports, tokens, or API keys. Before using or sharing the demo, audit already-tracked repository files: `.gitignore` does not remove content already committed, and deleting a file from the latest commit does not erase it from Git history.

For a safer test, copy the database to a separate local demo copy first. This app itself only opens the selected SQLite file in read-only mode.

## Test

```sh
python -m unittest discover -s demo -p 'test_*.py' -v
```

## Next engineering gate

Before adding semantic retrieval or autonomous actions, verify: (1) sensitive tracked files are removed from the public repository and history as appropriate, (2) schema mapping and evidence citations pass tests on a local database copy, and (3) every answer separates sourced facts, inference, and recommendations. Action execution must remain disabled until permissions, confirmation, and audit logging are implemented.
