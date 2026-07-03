import os
import re
import json
from pathlib import Path
from collections import defaultdict

# Comprehensive Python standard library (built-ins)
STD_LIBS = {
    'os', 'sys', 're', 'json', 'sqlite3', 'time', 'datetime', 'math', 'random',
    'collections', 'itertools', 'pathlib', 'subprocess', 'shutil', 'io', 'textwrap',
    'argparse', 'logging', 'typing', 'hashlib', 'uuid', 'tempfile', 'glob', 'csv',
    'string', 'stat', 'ast', 'asyncio', 'atexit', 'base64', 'binascii', 'bisect',
    'builtins', 'bz2', 'calendar', 'codecs', 'contextlib', 'copy', 'copyreg', 'ctypes',
    'dataclasses', 'decimal', 'difflib', 'distutils', 'email', 'encodings', 'enum',
    'errno', 'fileinput', 'fnmatch', 'fractions', 'functools', 'gc', 'getpass',
    'gettext', 'gzip', 'heapq', 'hmac', 'html', 'http', 'importlib', 'inspect',
    'ipaddress', 'keyword', 'linecache', 'locale', 'lzma', 'mimetypes', 'mmap',
    'msvcrt', 'multiprocessing', 'numbers', 'operator', 'optparse', 'pdb', 'pickle',
    'pkgutil', 'platform', 'plistlib', 'posixpath', 'pprint', 'py_compile', 'pydoc',
    'queue', 'reprlib', 'runpy', 'secrets', 'select', 'selectors', 'shlex', 'signal',
    'site', 'socket', 'ssl', 'stringprep', 'struct', 'sysconfig', 'tarfile', 'threading',
    'timeit', 'tkinter', 'token', 'tokenize', 'traceback', 'tracemalloc', 'types',
    'unicodedata', 'unittest', 'urllib', 'warnings', 'weakref', 'xml', 'xmlrpc',
    'zipfile', 'zipimport', 'zlib', 'zoneinfo'
}

def find_py_files(root_dir):
    py_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        # SKIP virtual environments and cache folders
        if 'venv' in dirpath or '__pycache__' in dirpath or '.git' in dirpath:
            continue
        for f in filenames:
            if f.endswith('.py'):
                py_files.append(os.path.join(dirpath, f))
    return py_files

def extract_imports(filepath):
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Match lines like: import x or from x import y
            matches = re.findall(r'^(?:from|import)\s+([a-zA-Z_][a-zA-Z0-9_\.]*)', content, re.MULTILINE)
            for m in matches:
                base = m.split('.')[0].strip()
                if base and base not in STD_LIBS:
                    imports.add(base)
    except Exception:
        pass
    return imports

def analyze_and_save():
    root = "."
    py_files = find_py_files(root)
    
    all_imports = set()
    
    print(f"🔍 Scanning {len(py_files)} Python files (skipping virtual envs)...")
    for i, f in enumerate(py_files):
        if i % 500 == 0:
            print(f"   Processed {i} files...")
        all_imports.update(extract_imports(f))

    third_party = sorted(list(all_imports))
    
    with open("requirements.txt", "w") as f:
        for pkg in third_party:
            f.write(pkg + "\n")
    
    print("\n✅ DONE! Cleaned requirements.txt generated.")
    print("📦 Packages detected: " + ", ".join(third_party))
    print("\n📄 Here's your clean list:\n" + "="*40)
    for pkg in third_party:
        print(f"- {pkg}")

if __name__ == "__main__":
    analyze_and_save()
