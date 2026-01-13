"""
INGV client module for the Earthquakes project.

This module is responsible for retrieving earthquake data from the
INGV (Istituto Nazionale di Geofisica e Vulcanologia) web services.

It:
- reads the geographic bounding box from the CSV file
- builds the query for the INGV API
- sends the HTTP request
- parses the response
- returns earthquake data in a structured format

This module does NOT handle:
- database operations
- command line parsing
- printing output
"""

import csv
import pathlib
import requests
from datetime import datetime, timedelta
from eq_package.write_boundingbox import write_bounding_box


def gather_earthquakes(days):
    """
    Fetch recent earthquake data from the INGV API within a
    specified time range and geographic bounding box.

    This function ensures that the bounding box file exists by calling
    `write_bounding_box()` if necessary, then reads the geographic coordinates
    from `bounding_box.csv`, queries the INGV API for earthquake data,
    and returns the results in a structured format.

    Args:
        days (int): Number of days in the past to fetch earthquake data for.

    Returns:
        list[tuple]: A list of earthquake records. Each tuple contains:
            - day (str): Date of the earthquake (YYYY-MM-DD format)
            - time (str): Time of the earthquake (HH:MM:SS format)
            - magnitude (float): Magnitude of the earthquake
            - latitude (float): Latitude of the earthquake epicenter
            - longitude (float): Longitude of the earthquake epicenter
            - place (str): Human-readable description of the location
    """

    # Step 1: Read the bounding box parameters from CSV file
    bounding_box = {}

    # Resolve path to data directory
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    csv_path = base_dir / "data" / "bounding_box.csv"

    # Create the CSV only if it does not exist yet
    if not csv_path.exists():
        write_bounding_box()

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
    """
        Manual test block for the ingv_client module.

        This block allows the module to be executed directly in order to:
        - fetch earthquake data for a fixed number of days
        - print the retrieved records to the console

        This is intended only for development and debugging purposes.
        """
    # Example: Fetch earthquakes from the last 7 days
    days = 7
    earthquakes = gather_earthquakes(days)
    print("Earthquake Data:")
    for eq in earthquakes:
        print(eq)
