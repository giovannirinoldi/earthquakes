import csv
import sqlite3
import math
import pathlib

import requests
from datetime import datetime, timedelta, timezone


def gather_earthquakes(days):
    """
    Fetch recent earthquake data from the INGV API within a
    specified time range and geographic bounding box.

    The function reads geographic bounding box coordinates from
    a CSV file named 'bounding_box.csv',
    queries the INGV API for earthquake data, and
    returns a list of tuples containing the earthquake details.

    Args:
        days (int):
        The number of days in the past to fetch earthquake data for.

    Returns:
    list: A list of tuples, where each tuple contains:
    - day (str): The date of the earthquake (YYYY-MM-DD format).
    - time (str): The time of the earthquake (HH:MM:SS format).
    - magnitude (float or None): The magnitude of the earthquake.
    - latitude (float): The latitude of the earthquake's epicenter.
    - longitude (float): The longitude of the earthquake's epicenter.
    - place (str): A human-readable description of the earthquake's location.
    """
    # Step 1: Read the bounding box parameters from CSV file
    bounding_box = {}

    csv_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "bounding_box.csv"

    with open(csv_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            bounding_box[row[0]] = float(row[1])

    # Step 2: Define the INGV API URL and query parameters
    url = "https://webservices.ingv.it/fdsnws/event/1/query?"
    start_time = (datetime.now() - timedelta(days=days)).isoformat()
    end_time = datetime.now().isoformat()
    params = {
        'format': 'geojson',
        'starttime': start_time,
        'endtime': end_time,
        'minlatitude': bounding_box['minlatitude'],
        'maxlatitude': bounding_box['maxlatitude'],
        'minlongitude': bounding_box['minlongitude'],
        'maxlongitude': bounding_box['maxlongitude'],
    }

    # Step 3: Query the INGV API for earthquake data
    response = requests.get(url, params=params)

    # Raise an HTTPError for bad responses (e.g., 404, 500)
    response.raise_for_status()
    data = response.json()

    # Step 4: Process the response and extract earthquake details
    events = data['features']  # Access the 'features' key directly
    earthquake_list = []

    for event in events:
        # Extract properties (metadata) and geometry (location) of the eq
        properties = event['properties']
        geometry = event['geometry']

        # Convert the ISO 8601 time field into UTC date and time
        timestamp = datetime.fromisoformat(
            properties['time']  # Parse the ISO 8601 time
        )
        day = timestamp.strftime('%Y-%m-%d')  # Format as "YYYY-MM-DD"
        time = timestamp.strftime('%H:%M:%S')  # Format as "HH:MM:SS"

        # Extract other earthquake details

        # Directly access 'mag' key
        magnitude = properties['mag']
        # Latitude is the second value in 'coordinates'
        latitude = geometry['coordinates'][1]
        # Longitude is the first value in 'coordinates'
        longitude = geometry['coordinates'][0]
        # Directly access 'place' key
        place = properties['place']

        # Append the earthquake details as a tuple
        earthquake_list.append(
            (day, time, magnitude, latitude, longitude, place)
        )

    # Step 5: Return the list of earthquake tuples
    return earthquake_list


# Optional: Test the function
if __name__ == "__main__":
    days = 7  # Example: Fetch earthquakes from the last 7 days
    earthquakes = gather_earthquakes(days)
    print("Earthquake Data:")
    for eq in earthquakes:
        print(eq)


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


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.

    Args:
        lat1 (float): Latitude of the first point in degrees.
        lon1 (float): Longitude of the first point in degrees.
        lat2 (float): Latitude of the second point in degrees.
        lon2 (float): Longitude of the second point in degrees.

    Returns:
        float: Distance in kilometers.
    """
    # Earth's radius in kilometers
    R = 6371.0

    # Convert coordinates from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance
    distance = R * c

    return distance


def get_closest_municipalities(eq_lat, eq_lon, n=5):
    """
    Find the n closest Italian municipalities to an earthquake epicenter.

    Args:
        eq_lat (float): Latitude of the earthquake epicenter.
        eq_lon (float): Longitude of the earthquake epicenter.
        n (int): Number of closest municipalities to return (default: 5).

    Returns:
        list[tuple]: List of tuples containing (municipality_name, distance_in_km).
    """
    municipalities = []

    # Resolve path to the right directory
    csv_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "italian_municipalities.csv"

    # Load municipalities from CSV
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row['name']
            lat = float(row['latitude'])
            lon = float(row['longitude'])

            # Calculate distance from earthquake epicenter
            distance = calculate_distance(eq_lat, eq_lon, lat, lon)
            municipalities.append((name, distance))

    # Sort by distance and return the n closest
    municipalities.sort(key=lambda x: x[1])
    return municipalities[:n]