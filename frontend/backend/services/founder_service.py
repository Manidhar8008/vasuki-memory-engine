import sqlite3

DB_PATH = "/data/data/com.termux/files/home/vasuki/vasuki_archaeologist/founder/founder.db"

class FounderService:

    def get_stats(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        stats = {}

        for table in [
            "documents",
            "entities",
            "founder_artifacts",
            "founder_memory"
        ]:
            try:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                stats[table] = cur.fetchone()[0]
            except:
                stats[table] = 0

        conn.close()

        return stats
