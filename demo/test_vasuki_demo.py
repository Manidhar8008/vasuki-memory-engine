import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("vasuki_demo.py")
spec = importlib.util.spec_from_file_location("vasuki_demo", MODULE_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)

class VasukiDemoTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "test.db"
        with sqlite3.connect(self.db) as c:
            c.executescript("""
                CREATE TABLE documents (id INTEGER PRIMARY KEY, title TEXT, content TEXT, path TEXT);
                CREATE TABLE founder_truths (id INTEGER PRIMARY KEY, truth_type TEXT, truth TEXT);
                INSERT INTO documents(title, content, path)
                    VALUES ('Vasuki architecture', 'Local first keeps private data on device', '/private/demo.md');
                INSERT INTO founder_truths(truth_type, truth)
                    VALUES ('DECISION', 'Prefer local-first architecture');
            """)
        app.DB_PATH = self.db.resolve()

    def tearDown(self):
        self.temp.cleanup()

    def test_summary_detects_schema_and_counts(self):
        result = app.summary()
        self.assertEqual(result["counts"]["documents"], 1)
        self.assertEqual(result["counts"]["founder_truths"], 1)
        self.assertEqual(result["mode"], "read-only")

    def test_search_returns_source_provenance(self):
        result = app.search("local first")
        self.assertGreaterEqual(result["count"], 1)
        self.assertTrue(any(r["source_table"] == "documents" for r in result["results"]))
        self.assertTrue(all("source_id" in r and "text" in r for r in result["results"]))

    def test_short_query_does_not_search(self):
        result = app.search("x")
        self.assertEqual(result["results"], [])

    def test_database_is_not_modified(self):
        before = self.db.stat().st_size
        app.summary()
        app.search("architecture")
        self.assertEqual(self.db.stat().st_size, before)

if __name__ == "__main__":
    unittest.main()
