import sqlite3
import pathlib
from eq_package.ingv_client import gather_earthquakes

def create_earthquake_db(days) -> None:
    """
    Create an SQLite database and populate it with recent earthquake data.

    This function:
    1. Calls the gather_earthquakes function and
        stores its output in a variable called 'earthquakes'.
    2. Creates (if it does not already exist) a table named 'earthquakes_db'
       with columns: day, time, mag, latitude, longitude, place.
    3. Inserts all earthquake records into the database using executemany.
    4. Closes the cursor and the database connection.

    Returns:
        None
    """
    # Retrieve earthquake data as a list of tuples:
    # (day, time, mag, latitude, longitude, place)
    earthquakes = gather_earthquakes(days)

    # Resolve path to data directory
    db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"

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
    INSERT OR IGNORE INTO earthquakes_db (day, time, mag, latitude, longitude, place)
    VALUES (?, ?, ?, ?, ?, ?);
    """

    # Insert all earthquake records into the database
    cursor.executemany(insert_sql, earthquakes)
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()


# Test the function
if __name__ == "__main__":
    days = 7
    create_earthquake_db()
    print("Database created and populated")

def query_db(k, days, min_magnitude) -> list[tuple]:
    """
    Query the earthquakes.db database for the strongest earthquakes.

    Returns at most k earthquakes with magnitude >= min_magnitude that occurred
    in the last `days` days, sorted by decreasing magnitude. (from tab earthquakes_db)

    Arguments:
        k (int): Maximum number of earthquakes to return.
        days (int): Number of past days to consider.
        min_magnitude (float): Minimum magnitude threshold.

    Returns:
        list[tuple]: List of tuples representing database rows.
    """
    # Calculate the minimum date to consider
    min_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    # Resolve path to data directory
    db_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "earthquakes.db"

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

    Arguments:
        earthquakes (list[tuple]): List of earthquake tuples.
    """
    for day, time, mag, lat, lon, place in earthquakes:
        print(
            f"day: {day}, time: {time}, magnitude: {mag}, "
            f"lat: {lat}, lon: {lon}, place: {place}"
        )

