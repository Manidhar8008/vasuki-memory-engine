import os
import subprocess
import datetime
from pathlib import Path

REPOS = [
    {"path": "~/vasuki", "name": "vasuki-memory-engine", "url": "https://github.com/Manidhar8008/vasuki-memory-engine.git"},
    {"path": "~/manidhar-portfolio", "name": "manidhar-portfolio", "url": "https://github.com/Manidhar8008/manidhar-portfolio.git"},
    {"path": "~/M-V1-portfolio-", "name": "M-V1-portfolio", "url": "https://github.com/Manidhar8008/M-V1-portfolio-.git"},
    {"path": "~/vasuki-explorer", "name": "vasuki-explorer", "url": None}  # No remote set yet
]

def get_git_remote(path):
    try:
        result = subprocess.run(["git", "-C", path, "remote", "get-url", "origin"], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def walk_files(root_dir):
    summary = []
    total_py = 0
    total_md = 0
    total_db = 0
    for dirpath, dirs, files in os.walk(root_dir):
        if 'venv' in dirpath or '__pycache__' in dirpath or '.git' in dirpath:
            continue
        for f in files:
            if f.endswith('.py'): total_py += 1
            elif f.endswith('.md'): total_md += 1
            elif f.endswith('.db'): total_db += 1
    return total_py, total_md, total_db

def generate_repo_doc(repo):
    path = os.path.expanduser(repo['path'])
    name = repo['name']
    
    if not os.path.exists(path):
        return f"*Repo `{name}` not found locally.*"
    
    remote = get_git_remote(path) or "Not set"
    py_count, md_count, db_count = walk_files(path)
    
    doc = f"# 📘 {name} - Checkpoint Report\n\n"
    doc += f"**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    doc += f"**Remote URL:** `{remote}`\n"
    doc += f"**Local Path:** `{path}`\n\n"
    doc += "## 📊 Stats at a Glance\n"
    doc += f"- **Python Files:** {py_count}\n"
    doc += f"- **Markdown Docs:** {md_count}\n"
    doc += f"- **SQLite Databases:** {db_count}\n\n"
    
    doc += "## 📂 File Structure (Top-Level)\n```\n"
    try:
        result = subprocess.run(["ls", "-la", path], capture_output=True, text=True)
        doc += result.stdout[:1500]  # Limit to avoid huge outputs
        doc += "\n... (truncated for brevity)\n```\n"
    except:
        doc += "Could not list files.\n```\n"
    
    doc += "\n## 🔑 Key Entry Points (Suggested)\n"
    doc += "> Based on `if __name__ == \"__main__\":` patterns\n"
    doc += "- Run `python explorer_api.py` (if exists) to start the web backend.\n"
    doc += "- Run `python seed_founder_answers.py` to populate the database.\n"
    
    return doc

def generate_master_ecosystem():
    doc = "# 🌐 Vasuki Ecosystem - Global Checkpoint\n\n"
    doc += f"**Checkpoint Date:** {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
    doc += "This document summarizes all active repositories and their relationships.\n\n"
    doc += "## 📌 Repository Map\n"
    for repo in REPOS:
        doc += f"- **{repo['name']}** → `{repo['url'] or 'No remote set'}`\n"
    doc += "\n## 🧠 What is this system?\n"
    doc += "This is a **Personal AI Memory Engine** built over months. It consists of:\n"
    doc += "- **Backend API** (FastAPI) for querying and serving memory.\n"
    doc += "- **Agents & Brain** for AI reasoning, classification, and semantic search.\n"
    doc += "- **Knowledge Graphs & SQLite DBs** storing tens of thousands of data points.\n"
    doc += "- **Portfolio & Frontend** components for public-facing interaction.\n\n"
    doc += "## ✅ Next Steps for Development\n"
    doc += "1. Consolidate the `backend` and `explorer_api` into a single unified API.\n"
    doc += "2. Write a comprehensive `README.md` for each repository.\n"
    doc += "3. Set up CI/CD (GitHub Actions) to auto-build the database on push.\n"
    return doc

def main():
    print("📝 Generating documentation checkpoint...")
    
    # Generate repo-specific docs
    for repo in REPOS:
        path = os.path.expanduser(repo['path'])
        doc_path = os.path.join(path, f"CHECKPOINT_{datetime.datetime.now().strftime('%Y%m%d')}.md")
        content = generate_repo_doc(repo)
        with open(doc_path, "w") as f:
            f.write(content)
        print(f"  ✅ Created {doc_path}")
    
    # Generate global ecosystem doc
    master_path = os.path.expanduser("~/vasuki/ECOSYSTEM_CHECKPOINT.md")
    with open(master_path, "w") as f:
        f.write(generate_master_ecosystem())
    print(f"  ✅ Created {master_path}")

if __name__ == "__main__":
    main()
