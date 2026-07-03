import os
import re
import sys
import json
from pathlib import Path
from collections import defaultdict

# Standard library modules (common ones to filter out)
STD_LIBS = {
    'sys', 'os', 're', 'json', 'sqlite3', 'time', 'datetime', 'math', 
    'random', 'collections', 'itertools', 'pathlib', 'subprocess', 
    'shutil', 'io', 'textwrap', 'argparse', 'logging', 'typing', 
    'hashlib', 'uuid', 'tempfile', 'glob', 'csv', 'string', 'stat'
}

def find_py_files(root_dir):
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.py') and '__pycache__' not in dirpath:
                py_files.append(os.path.join(dirpath, f))
    return py_files

def extract_imports(filepath):
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match: import x, import x as y, from x import y
            matches = re.findall(r'^(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', content, re.MULTILINE)
            for m in matches:
                # Clean up: if it's "from x.y import z", we take 'x'
                base = m.split('.')[0]
                imports.add(base)
    except Exception:
        pass
    return imports

def find_entry_points(py_files):
    entry_points = []
    for f in py_files:
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                content = fp.read()
                # Check for main guard or typical web framework patterns
                if 'if __name__ == "__main__":' in content:
                    entry_points.append(f)
                elif 'app.run(' in content or 'uvicorn.run' in content or 'FastAPI()' in content:
                    entry_points.append(f)
        except Exception:
            pass
    return entry_points

def analyze_project(root_dir):
    root = Path(root_dir)
    py_files = find_py_files(root_dir)
    all_imports = set()
    file_map = {}
    
    for f in py_files:
        rel_path = os.path.relpath(f, root_dir)
        imports = extract_imports(f)
        all_imports.update(imports)
        file_map[rel_path] = list(imports)
    
    third_party = sorted([pkg for pkg in all_imports if pkg not in STD_LIBS and not pkg.startswith('_')])
    entry_points = find_entry_points(py_files)
    entry_points_rel = [os.path.relpath(f, root_dir) for f in entry_points]
    
    # Detect databases
    dbs = [str(f) for f in root.glob('*.db')]
    
    # Detect env and readme
    env = (root / '.env').exists()
    readme = (root / 'README.md').exists()
    
    return {
        'total_py_files': len(py_files),
        'third_party_packages': third_party,
        'entry_points': entry_points_rel,
        'databases': dbs,
        'has_env': env,
        'has_readme': readme,
        'file_imports': file_map
    }

def generate_report(data):
    lines = []
    lines.append("# Vasuki Memory Engine - Project Analysis")
    lines.append("")
    lines.append(f"**Total Python Files:** {data['total_py_files']}")
    lines.append(f"**Has .env:** {'Yes' if data['has_env'] else 'No'}")
    lines.append(f"**Has README.md:** {'Yes' if data['has_readme'] else 'No'}")
    lines.append("")
    
    lines.append("## 🚀 Main Entry Points (Run these)")
    for e in data['entry_points']:
        lines.append(f"- `python {e}`")
    if not data['entry_points']:
        lines.append("- No clear entry point detected.")
    
    lines.append("")
    lines.append("## 📦 Required Third-Party Packages")
    if data['third_party_packages']:
        for pkg in data['third_party_packages']:
            lines.append(f"- {pkg}")
    else:
        lines.append("- No third-party packages detected (only stdlib).")
    
    lines.append("")
    lines.append("## 🗄️ Detected SQLite Databases")
    for db in data['databases']:
        lines.append(f"- `{db}`")
    
    lines.append("")
    lines.append("## 📁 File Import Map (Sample)")
    for i, (f, imports) in enumerate(data['file_imports'].items()):
        if i < 15: # limit to first 15 to keep report clean
            lines.append(f"- `{f}` → {imports}")
    if len(data['file_imports']) > 15:
        lines.append(f"- *... and {len(data['file_imports']) - 15} more files.*")
    
    return "\n".join(lines)

if __name__ == "__main__":
    print("🔍 Analyzing your Vasuki project...")
    results = analyze_project(".")
    
    # Write requirements.txt
    with open("requirements.txt", "w") as f:
        for pkg in results['third_party_packages']:
            f.write(pkg + "\n")
    
    # Write summary report
    with open("PROJECT_SUMMARY.md", "w") as f:
        f.write(generate_report(results))
    
    print("✅ Done! Files created:")
    print("   - requirements.txt (use `pip install -r requirements.txt`)")
    print("   - PROJECT_SUMMARY.md (full structure overview)")
    print("\n📄 Here's the summary:\n" + "="*40)
    print(generate_report(results))
