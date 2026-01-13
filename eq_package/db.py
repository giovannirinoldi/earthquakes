"""
Database utilities for the Earthquakes project.

This module contains functions to:
- create and populate a local SQLite database with earthquake data
- query the database for the strongest earthquakes given constraints
- print earthquake records in the required output format

Database location:
    The SQLite database file is saved in the `data/` folder as:
        data/earthquakes.db

Table schema:
    earthquakes_db(
        day TEXT,
        time TEXT,
        mag REAL,
        latitude REAL,
        longitude REAL,
        place TEXT
    )

Notes:
    - Earthquake data are retrieved via `gather_earthquakes(days)`.
    - Duplicates prevention using a UNIQUE constraint and `INSERT OR IGNORE`.
"""

import sqlite3
import pathlib
from eq_package.ingv_client import gather_earthquakes
from datetime import datetime, timedelta


def create_earthquake_db(days) -> None:
    """
    Create (if needed) and populate the SQLite database with earthquake data.

    Workflow:
        1) Fetch earthquakes from INGV for the last `days` days using
           `gather_earthquakes(days)`.
        2) Create the `earthquakes_db` table if it does not already exist.
        3) Insert earthquake records into the table (duplicates are ignored).
        4) Close the database connection.

    Args:
        days (int): Days in the past for which to fetch earthquake data.

    Returns:
        None
    """
    # Retrieve earthquake data as a list of tuples:
    # (day, time, mag, latitude, longitude, place)
    earthquakes = gather_earthquakes(days)

    # Resolve path to data directory
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "earthquakes.db"

    # Open a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL statement to create the table if it does not already exist
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS earthquakes_db (
        day TEXT,
        time TEXT,
        mag REAL,
        latitude REAL,
        longitude REAL,
        place TEXT,
        UNIQUE(day, time, mag, latitude, longitude, place)
    );
    """

    # Execute the CREATE TABLE statement
    cursor.execute(create_table_sql)
    conn.commit()

    # SQL statement to insert data into the table
    insert_sql = """
    INSERT OR IGNORE INTO earthquakes_db
    (day, time, mag, latitude, longitude, place)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    # Insert all earthquake records into the database
    cursor.executemany(insert_sql, earthquakes)
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()


# Optional: Test the function
if __name__ == "__main__":
    """
    Manual test entrypoint.

    Note:
        This block is meant for quick manual checks. The production entrypoint
        for the project should be the interface (argparse) module.
    """
    # Example: Fetch earthquakes from the last 7 days
    days = 7
    create_earthquake_db()
    print("Database created and populated")


def query_db(k, days, min_magnitude) -> list[tuple]:
    """
    Query the earthquakes database for the strongest earthquakes.

    The query returns at most `k` earthquakes that:
    - have magnitude >= `min_magnitude`
    - occurred within the last `days` days
    Results are sorted by decreasing magnitude.

    Args:
        k (int): Maximum number of earthquakes to return.
        days (int): Number of past days to consider.
        min_magnitude (float): Minimum magnitude threshold.

    Returns:
        list[tuple]: List of rows in the format:
            (day, time, mag, latitude, longitude, place)
    """
    # Calculate the minimum date to consider
    min_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Resolve path to data directory
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    db_path = base_dir / "data" / "earthquakes.db"

    # Connect to the db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Write the query
    query_sql = """
    SELECT day, time, mag, latitude, longitude, place
    FROM earthquakes_db
    WHERE mag >= ?
    AND day >= ?
    ORDER BY mag DESC
    LIMIT ?;
    """

    # Query the db with parameters
    cursor.execute(query_sql, (min_magnitude, min_date, k))
    results = cursor.fetchall()

    # Close connection
    cursor.close()
    conn.close()

    return results


def print_earthquakes(earthquakes) -> None:
    """
    Print earthquake records in the required formatted style.

    Each record is printed on one line using the format:
        day: <day>, time: <time>,
        magnitude: <mag>, lat: <lat>,
        lon: <lon>, place: <place>

    Args:
        earthquakes (list[tuple]): List of earthquake tuples in the format:
            (day, time, mag, lat, lon, place)

    Returns:
        None
    """
    for day, time, mag, lat, lon, place in earthquakes:
        print(
            f"day: {day}, time: {time}, magnitude: {mag}, "
            f"lat: {lat}, lon: {lon}, place: {place}"
        )
