import csv
import math
import pathlib

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