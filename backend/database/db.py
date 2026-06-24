import sqlite3

DB = "/data/data/com.termux/files/home/vasuki/vasuki.db"

def get_db():
    return sqlite3.connect(DB)
