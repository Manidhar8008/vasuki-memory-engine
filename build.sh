#!/data/data/com.termux/files/usr/bin/bash

mkdir -p providers skills memory logs cache

touch \
config.py \
database.py \
memory.py \
brain.py \
router.py \
main.py \
providers/nvidia.py \
skills/remember.py \
skills/status.py \
skills/help.py

echo "✅ Vasuki structure created."
