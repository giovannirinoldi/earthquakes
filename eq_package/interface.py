import argparse

from eq_package.municipalities import get_closest_municipalities
from eq_package.db import create_earthquake_db, query_db, print_earthquakes

def main():
    # Create an argument parser object
    parser = argparse.ArgumentParser(
        description="Fetch the strongest earthquakes in Italy within the specified number of days, based on the given magnitude and count (K)."
    )

    # Add arguments
    parser.add_argument(
        "--days",
        type=int,
        required=True,
        help="Number of days in the past to fetch earthquake data for."
    )
    parser.add_argument(
        "--K",
        type=int,
        required=True,
        help="The maximum number of strongest earthquakes to return."
    )
    parser.add_argument(
        "--magnitude",
        type=float,
        required=True,
        help="The minimum magnitude of earthquakes to consider."
    )
    parser.add_argument(
        "--closest-municipalities",
        action="store_true",
        help="Show the 5 closest Italian municipalities for each earthquake."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Print the parsed arguments (For now, just to verify the input)
    #print(f"Days: {args.days}, K: {args.K}, Magnitude: {args.magnitude}")

    create_earthquake_db(args.days)

    # Call query_db with user inputs
    earthquakes = query_db(args.K, args.days, args.magnitude)

    # Print the results in the required format
    if args.closest_municipalities:
        # Print with closest municipalities
        for day, time, mag, lat, lon, place in earthquakes:
            print(
                f"day: {day}, time: {time}, magnitude: {mag}, "
                f"lat: {lat}, lon: {lon}, place: {place}"
            )
            # Get and print the 5 closest municipalities
            closest = get_closest_municipalities(lat, lon, n=5)
            for municipality, distance in closest:
                print(f"  - {municipality}: {distance:.2f} km")
    else:
        # Use original output format
        print_earthquakes(earthquakes)
