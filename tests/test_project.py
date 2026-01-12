"""

"""

import unittest
from unittest import TestCase
import csv
import sqlite3
from eq_package.db import create_earthquake_db, query_db
from eq_package.write_boundingbox import write_bounding_box
import pathlib


class TestProject(TestCase):
    @classmethod
    def setUpClass(cls):
        """Ensure earthquakes.db exists before running tests."""
        db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"
        if not db_path.exists():
            print("Creating earthquakes.db...")
            create_earthquake_db(days=30)

    def test_bounding_box(self):
        """Test that specific Italian cities are within the bounding box."""
        # Read bounding_box.csv
        bounding_box = {}
        # Resolve path to data directory
        csv_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "bounding_box.csv"
        # Create the CSV only if it does not exist yet
        if not csv_path.exists():
            write_bounding_box()

        with open(csv_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                bounding_box[row[0]] = float(row[1])

        # Test coordinates
        test_cities = {
            'Padova': (45.4064, 11.8768),
            'Parma': (44.8015, 10.3279),
            'Palermo': (38.1157, 13.3615)
        }

        for city, (lat, lon) in test_cities.items():
            with self.subTest(city=city):
                self.assertGreaterEqual(lat, bounding_box['minlatitude'],
                                        f"{city} latitude too small")
                self.assertLessEqual(lat, bounding_box['maxlatitude'],
                                     f"{city} latitude too large")
                self.assertGreaterEqual(lon, bounding_box['minlongitude'],
                                        f"{city} longitude too small")
                self.assertLessEqual(lon, bounding_box['maxlongitude'],
                                     f"{city} longitude too large")

    def test_magnitude(self):
        """Test that no earthquake has magnitude greater than 9.5."""
        # Ensure database exists
        db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"
        if not db_path.exists():
            create_earthquake_db(days=30)

        # Query database directly
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(mag) FROM earthquakes_db")
        max_magnitude = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Assert no earthquake exceeds 9.5
        if max_magnitude is not None:
            self.assertLessEqual(max_magnitude, 9.5,
                                 "Found earthquake with magnitude > 9.5")

    def test_order(self):
        """Test that query_db returns earthquakes sorted by decreasing magnitude."""
        # Ensure database exists
        db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"
        if not db_path.exists():
            create_earthquake_db(days=30)

        # Query the database
        earthquakes = query_db(k=10, days=30, min_magnitude=1.0)

        # Extract magnitudes
        magnitudes = [eq[2] for eq in earthquakes]  # mag is at index 2

        # Assert the list is sorted in decreasing order
        self.assertEqual(magnitudes, sorted(magnitudes, reverse=True),
                         "Earthquakes are not sorted by decreasing magnitude")

    def test_database_has_data(self):
        """Test that the database contains at least one earthquake record."""
        # Ensure database exists
        db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"
        if not db_path.exists():
            create_earthquake_db(days=30)

        # Query database for row count
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM earthquakes_db")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Assert database is not empty
        self.assertGreater(count, 0,
                           "Database should contain at least one earthquake record")


if __name__ == "__main__":
    unittest.main()
