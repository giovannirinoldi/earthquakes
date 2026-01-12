import csv
import pathlib
import requests
from datetime import datetime, timedelta

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