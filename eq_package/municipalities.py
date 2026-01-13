"""
Municipalities utilities for the Earthquakes project.

This module provides functions to work with Italian municipalities data.

Main responsibilities:
- compute geographic distances between coordinates (Haversine formula)
- find the closest Italian municipalities to a given earthquake epicenter

Data source:
    The module expects a CSV file named `italian_municipalities.csv` stored
    in the `data/` directory (sibling of the package directory).

Expected CSV columns:
    - name: municipality name (string)
    - latitude: latitude in decimal degrees (float)
    - longitude: longitude in decimal degrees (float)

Typical usage:
    closest = get_closest_municipalities(eq_lat, eq_lon, n=5)
    for name, km in closest:
        print(name, km)
"""

import csv
import math
import pathlib


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth.
    The Haversine formula is used.

    The Haversine formula returns the great-circle distance between two points
    on a sphere from their longitudes and latitudes.

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
    a = (math.sin(dlat / 2)**2
         + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
         )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate distance
    distance = R * c

    return distance


def get_closest_municipalities(eq_lat, eq_lon, n=5):
    """
    Find the `n` closest Italian municipalities to an earthquake epicenter.

    This function loads the municipalities dataset from:
        data/italian_municipalities.csv

    For each municipality, it computes the great-circle distance (in km)
    from the earthquake epicenter (eq_lat, eq_lon)
    and returns the closest `n` results.

    Args:
        eq_lat (float): Latitude of the earthquake epicenter (decimal degrees)
        eq_lon (float): Longitude of the earthquake epicenter (decimal degrees)
        n (int): Number of closest municipalities to return (default: 5)

    Returns:
        list[tuple]: List of tuples (municipality_name, distance_km), sorted by
        increasing distance, with length at most `n`.
    """
    municipalities = []

    # Resolve path to data directory
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    csv_path = base_dir / "data" / "italian_municipalities.csv"

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
