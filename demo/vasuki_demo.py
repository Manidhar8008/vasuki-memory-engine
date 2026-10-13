#!/usr/bin/env python3
"""Vasuki Founder OS — local-only, read-only MVP.

Run: python demo/vasuki_demo.py [path/to/vasuki.db]
Open: http://127.0.0.1:8765
No uploads, no cloud calls, no database writes. Binds loopback only.
"""
from __future__ import annotations
import json, os, sqlite3, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

HOST, PORT = "127.0.0.1", int(os.environ.get("VASUKI_PORT", "8765"))
DB_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("VASUKI_DB", "~/vasuki/vasuki.db")).expanduser().resolve()
MAX_RESULTS = 40
SAFE_TABLES = {
    "documents": ["title", "content", "path"],
    "memories": ["memory", "memory_type"],
    "founder_truths": ["truth", "truth_type"],
    "projects": ["name", "title", "description", "status"],
    "goals": ["name", "title", "description", "status"],
    "decisions": ["name", "title", "description", "decision"],
    "learnings": ["name", "title", "description", "learning"],
    "events": ["name", "title", "description", "event"],
    "notes": ["title", "content", "note"],
    "founder_notes": ["title", "content", "note"],
    "founder_observations": ["observation", "content", "note"],
    "artifacts": ["source", "path", "content"],
    "artifacts_v2": ["source", "path", "content"],
}

def connect():
    if not DB_PATH.is_file():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    # SQLite immutable/read-only connection; never creates or modifies the database.
    uri = DB_PATH.as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True, timeout=2)

def table_info(conn):
    names = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")]
    result = []
    for name in names:
        cols = [r[1] for r in conn.execute(f'PRAGMA table_info("{name.replace(chr(34), chr(34)*2)}")')]
        result.append({"name": name, "columns": cols})
    return result

def summary():
    with connect() as c:
        info = table_info(c)
        tables = {x["name"]: x["columns"] for x in info}
        counts = {}
        for t in ("documents", "memories", "entities", "projects", "goals", "decisions", "learnings", "events", "founder_truths", "ontology_objects"):
            if t in tables:
                try:
                    counts[t] = c.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
                except sqlite3.Error:
                    counts[t] = None
        return {"database": str(DB_PATH), "tables": len(info), "counts": counts,
                "searchable_tables": [t for t, cols in SAFE_TABLES.items() if t in tables and any(x in cols for x in tables[t])],
                "mode": "read-only", "binding": HOST}

def search(q):
    q = q.strip()[:180]
    if len(q) < 2:
        return {"query": q, "results": [], "note": "Enter at least two characters."}
    terms = q.split()[:6]
    results = []
    with connect() as c:
        existing = {x["name"]: x["columns"] for x in table_info(c)}
        for table, candidates in SAFE_TABLES.items():
            if table not in existing:
                continue
            cols = [col for col in candidates if col in existing[table]]
            if not cols:
                continue
            # Bound each search term; table/column identifiers come only from the inspected schema.
            clauses, params = [], []
            for term in terms:
                per_term = []
                for col in cols:
                    per_term.append(f'CAST("{col}" AS TEXT) LIKE ?')
                    params.append("%" + term.replace("%", "\\%").replace("_", "\\_") + "%")
                clauses.append("(" + " OR ".join(per_term) + ")")
            sql = f'SELECT rowid, ' + ", ".join(f'"{col}"' for col in cols) + f' FROM "{table}" WHERE ' + " AND ".join(clauses) + " LIMIT ?"
            params.append(MAX_RESULTS - len(results))
            try:
                rows = c.execute(sql, params).fetchall()
            except sqlite3.Error:
                continue
            for row in rows:
                body = " | ".join(f"{col}: {str(val)[:900]}" for col, val in zip(cols, row[1:]) if val not in (None, ""))
                results.append({"source_table": table, "source_id": row[0], "text": body})
                if len(results) >= MAX_RESULTS:
                    break
            if len(results) >= MAX_RESULTS:
                break
    return {"query": q, "results": results, "count": len(results), "note": "Keyword retrieval only; results are evidence candidates, not verified conclusions."}

PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>VASUKI · Founder OS</title>
<style>
:root{color-scheme:dark;--bg:#0a0e13;--panel:#111923;--line:#253241;--text:#e6edf5;--muted:#8da0b5;--cyan:#62d8e8;--amber:#f0bc72}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 70% -10%,#16313d 0,transparent 42%),var(--bg);color:var(--text);font:15px/1.5 system-ui,-apple-system,sans-serif}
header{padding:24px clamp(16px,4vw,52px);border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:16px}
.brand{letter-spacing:.18em;font-size:12px;color:var(--cyan);font-weight:800}.sub{color:var(--muted);font-size:12px}.tag{border:1px solid #765c38;color:var(--amber);padding:5px 9px;border-radius:20px;font-size:11px;white-space:nowrap}
main{max-width:1250px;margin:auto;padding:28px clamp(16px,4vw,52px) 60px}.eyebrow{color:var(--cyan);font-size:11px;letter-spacing:.17em;text-transform:uppercase}
h1{font-size:clamp(28px,4vw,46px);line-height:1.05;margin:8px 0 12px;letter-spacing:-.04em}.lead{color:var(--muted);max-width:700px}
.grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin:28px 0}.metric,.panel{background:linear-gradient(145deg,#141e29,#0f151e);border:1px solid var(--line);border-radius:13px;padding:17px}.metric .num{font-size:25px;font-weight:750;letter-spacing:-.04em;margin-top:7px}.metric .label{font-size:12px;color:var(--muted)}
.columns{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(260px,1fr);gap:14px}.panel h2{font-size:15px;margin:0 0 12px}.searchrow{display:flex;gap:8px}input{min-width:0;flex:1;background:#080d12;border:1px solid #304052;border-radius:8px;color:var(--text);padding:12px;font:inherit}button{background:var(--cyan);color:#071216;border:0;border-radius:8px;padding:10px 15px;font-weight:750;cursor:pointer}
.result{padding:13px 0;border-bottom:1px solid var(--line);overflow-wrap:anywhere}.result:last-child{border:0}.source{color:var(--cyan);font-size:11px;letter-spacing:.06em}.snippet{color:#c2cfdb;font-size:13px;margin-top:5px;white-space:pre-wrap}
.list{display:grid;gap:8px}.item{border:1px solid var(--line);border-radius:9px;padding:11px}.item b{font-size:13px}.item p{color:var(--muted);font-size:12px;margin:4px 0 0}
.notice{margin-top:14px;color:var(--muted);font-size:12px}.status{display:inline-block;width:7px;height:7px;border-radius:50%;background:#78d6a5;margin-right:7px}
footer{color:var(--muted);font-size:11px;margin-top:24px}
@media(max-width:850px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.columns{grid-template-columns:1fr}.grid .metric:last-child{grid-column:span 2}}@media(min-width:851px){.grid .metric:last-child{grid-column:auto}}
</style></head>
<body>
<header><div><div class="brand">VASUKI <span style="color:#fff">/</span> FOUNDER OS</div><div class="sub">Personal intelligence · local runtime</div></div><div class="tag">LOCAL · READ ONLY</div></header>
<main><div class="eyebrow">Founder intelligence system / MVP</div><h1>Context, connected.<br><span style="color:var(--cyan)">Evidence, visible.</span></h1>
<p class="lead">Explore your own indexed knowledge without modifying the source database. Search returns source-linked evidence candidates; it does not pretend keyword matches are reasoning.</p>
<div class="grid" id="metrics"><div class="metric"><div class="label">DATABASE</div><div class="num">…</div></div></div>
<div class="columns"><section class="panel"><h2>Ask Vasuki · evidence search</h2><form id="searchform"><div class="searchrow"><input id="q" placeholder="e.g. Vasuki, local first, goals…" autocomplete="off" minlength="2"><button>Search</button></div></form><div class="notice">Searches selected columns in the connected local database. Up to 40 results.</div><div id="results" aria-live="polite"></div></section>
<aside class="panel"><h2>System state</h2><div class="list" id="state"><div class="item">Checking local database…</div></div><p class="notice">V1 is intentionally read-only. No action execution, cloud sync, uploads, or hidden collection.</p></aside></div>
<footer><span class="status"></span>Bound to 127.0.0.1 · SQLite read-only · No third-party requests from this page</footer></main>
<script>
const fmt=n=>n==null?'—':Number(n).toLocaleString();
async function load(){try{const r=await fetch('/api/summary');const d=await r.json();const metrics=document.querySelector('#metrics');metrics.innerHTML='';const preferred=[['documents','Documents'],['memories','Memories'],['entities','Entities'],['ontology_objects','Ontology'],['founder_truths','Founder truths']];for(const [k,label] of preferred){const el=document.createElement('div');el.className='metric';el.innerHTML='<div class="label">'+label+'</div><div class="num">'+fmt(d.counts[k])+'</div>';metrics.append(el)}const state=document.querySelector('#state');state.innerHTML='';[['Connection', 'Connected · read-only'],['Tables discovered',fmt(d.tables)],['Search sources',d.searchable_tables.join(', ')||'None detected'],['Database path',d.database]].forEach(([k,v])=>{const el=document.createElement('div');el.className='item';const b=document.createElement('b');b.textContent=k;const p=document.createElement('p');p.textContent=v;el.append(b,p);state.append(el)})}catch(e){document.querySelector('#metrics').innerHTML='<div class="metric"><div class="label">DATABASE</div><div class="num">Offline</div></div>';document.querySelector('#state').textContent='Could not open database. Start the server with the correct database path; details are in the terminal.'}}
document.querySelector('#searchform').addEventListener('submit',async e=>{e.preventDefault();const q=document.querySelector('#q').value;const box=document.querySelector('#results');box.textContent='Searching…';try{const d=await (await fetch('/api/search?q='+encodeURIComponent(q))).json();box.innerHTML='';if(!d.results.length){box.textContent=d.note||'No matches found.';return}for(const item of d.results){const el=document.createElement('div');el.className='result';const src=document.createElement('div');src.className='source';src.textContent=item.source_table+' · row '+item.source_id;const body=document.createElement('div');body.className='snippet';body.textContent=item.text;el.append(src,body);box.append(el)}const n=document.createElement('div');n.className='notice';n.textContent=d.count+' evidence candidates · '+d.note;box.prepend(n)}catch(err){box.textContent='Search failed. Check the server terminal.'}});
load();
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("%s - %s" % (self.client_address[0], fmt % args))
    def send_json(self, obj, status=200):
        data = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status); self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data))); self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff"); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        route = urlparse(self.path)
        try:
            if route.path == "/":
                data = PAGE.encode()
                self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(data))); self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'self'; img-src 'self' data:")
                self.end_headers(); self.wfile.write(data)
            elif route.path == "/api/health":
                self.send_json({"ok": True, "mode": "read-only", "database_exists": DB_PATH.is_file()})
            elif route.path == "/api/summary":
                self.send_json(summary())
            elif route.path == "/api/search":
                self.send_json(search(parse_qs(route.query).get("q", [""])[0]))
            else:
                self.send_json({"error": "Not found"}, 404)
        except FileNotFoundError as e:
            self.send_json({"error": str(e), "hint": "Pass your local database path as the first argument."}, 404)
        except Exception as e:
            self.send_json({"error": type(e).__name__, "detail": str(e)[:300]}, 500)

if __name__ == "__main__":
    print("VASUKI Founder OS MVP")
    print(f"Database: {DB_PATH}")
    print(f"Mode: read-only | Listening: http://{HOST}:{PORT}")
    print("Stop with Ctrl+C. This server must remain bound to 127.0.0.1.")
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
