import sqlite3

DB_PATH = "data/portfolio.db"

def get_db():
    return sqlite3.connect(DB_PATH)
