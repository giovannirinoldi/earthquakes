"""
Unit tests for the Earthquakes project.

This test module is located in the `tests/` folder, which is a sibling of:
- `eq_package/` (the Python package with the project code)
- `data/` (project data folder)

The tests validate the core requirements described in the lab instructions:
- bounding box correctness (Padova, Parma, Palermo must be inside)
- magnitude sanity check (no earthquake magnitude > 9.5)
- ordering of query results (sorted by decreasing magnitude)
- one additional sanity test (database not empty)

How to run:
    python -m unittest tests/test_project.py
"""

import unittest
from unittest import TestCase
import csv
import sqlite3
from eq_package.db import create_earthquake_db, query_db
from eq_package.write_boundingbox import write_bounding_box
import pathlib


class TestProject(TestCase):
    """
    Test suite for the Earthquakes project.

    This class uses `setUpClass` to ensure that required files exist:
    - `data/earthquakes.db` (created by create_earthquake_db)
    - `data/bounding_box.csv` (created by write_bounding_box when needed)

    Individual tests assume these resources are available.
    """
    @classmethod
    def setUpClass(cls):
        """
        Create required resources once for the entire test class.

        This setup:
        - ensures `data/` exists
        - creates `data/bounding_box.csv` if missing (static config)
        - creates `data/earthquakes.db` if missing (dynamic data)
        """
        # Check for 'data' folder
        data_dir = pathlib.Path(__file__).resolve().parent.parent / "data"
        data_dir.mkdir(exist_ok=True)

        # Files paths
        cls.csv_path = data_dir / "bounding_box.csv"
        cls.db_path = data_dir / "earthquakes.db"

        # Check for bounding_box.csv
        if not cls.csv_path.exists():
            print("Creating bounding_box.csv...")
            write_bounding_box()

        # Check for database
        if not cls.db_path.exists():
            print("Creating earthquakes.db...")
            create_earthquake_db(days=30)

    def test_bounding_box(self):
        """
        Test that Padova, Parma and Palermo are inside the bounding box.

        The test reads `data/bounding_box.csv` and verifies that each city's
        latitude/longitude fall inside the min/max boundaries.
          """
        # Initialize dictionary
        bounding_box = {}
        # Read bounding_box.csv
        with open(self.csv_path, mode='r') as file:
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
        """
        Test that no earthquake stored in the database exceeds magnitude 9.5.

        The test queries the maximum magnitude from the `earthquakes_db` table.
        """
        # Query database directly
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(mag) FROM earthquakes_db")
        max_magnitude = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Assert no earthquake exceeds 9.5
        if max_magnitude is not None:
            self.assertLessEqual(
                max_magnitude, 9.5, "Found earthquake with magnitude > 9.5"
            )

    def test_order(self):
        # Query the database
        earthquakes = query_db(k=10, days=30, min_magnitude=1.0)

        # Extract magnitudes
        magnitudes = [eq[2] for eq in earthquakes]  # mag is at index 2

        # Assert the list is sorted in decreasing order
        self.assertEqual(magnitudes, sorted(magnitudes, reverse=True),
                         "Earthquakes are not sorted by decreasing magnitude")

    def test_database_has_data(self):
        """Test that the database contains at least one earthquake record."""
        # Query database for row count
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM earthquakes_db")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        # Assert database is not empty
        self.assertGreater(
            count, 0, "Database should contain at least one earthquake record"
        )


if __name__ == "__main__":
    """
    Allow running this module directly.
    """
    unittest.main()
