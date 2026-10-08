import os
import tempfile
import unittest
from pathlib import Path

from agriql import connect
from agriql.result import Result


class ClientTest(unittest.TestCase):
    def test_memory_query_uses_the_engine(self):
        db = connect(":memory:")
        text = db.query("SHOW VERSION;").text
        self.assertIn("engine=3.10.1", text)
        db.close()

    def test_aqdb_file_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["AGRIQL_DATA_DIR"] = tmp
            created = connect(":memory:")
            created.query("CREATE DATABASE farm;")
            created.close()
            path = Path(tmp) / "databases" / "farm.aqdb"
            self.assertTrue(path.is_file(), path)
            db = connect(str(path))
            db.query("CREATE SCHEMA fields;")
            db.close()
            again = connect(str(path))
            self.assertIn("fields", again.query("SHOW SCHEMAS;").text)
            again.close()

    def test_records_and_missing_optional_libraries(self):
        result = Result("plant_id\tsoil_moisture\na\t10\n")
        self.assertEqual(result.to_records(), [{"plant_id": "a", "soil_moisture": "10"}])
        with self.assertRaises(ImportError):
            result.to_pandas()
        with self.assertRaises(ImportError):
            result.to_polars()
        with self.assertRaises(ImportError):
            result.to_arrow()


if __name__ == "__main__":
    unittest.main()
