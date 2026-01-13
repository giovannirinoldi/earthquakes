"""
Command-line interface for the Earthquakes project.

This module defines the main entry point for the application when used from
the command line. It is responsible for:

- parsing user arguments using argparse
- orchestrating the execution flow of the program
- invoking database creation and queries
- optionally retrieving closest italian municipalities
- printing results in the required format

This module does NOT:
- fetch earthquake data directly
- handle database logic
- manage CSV files

Those responsibilities are delegated to the corresponding modules.
"""

import argparse
from eq_package.municipalities import get_closest_municipalities
from eq_package.db import create_earthquake_db, query_db, print_earthquakes


def main():
    """
    Main entry point for the Earthquakes command-line application.

    This function:
    - Parses command-line arguments provided by the user
    - Creates or updates the local SQLite database with recent earthquake data
    - Queries the database for the strongest earthquakes matching the criteria
    - Prints the results to standard output
    - (Optional) print the closest italian municipalities for each earthquake

    Expected command-line arguments:
    --days (int, required): Days in the past to fetch earthquake data for
    --K (int, required): Maximum number of strongest earthquakes to return
    --magnitude (float, required): Minimum magnitude of earthquakes to consider
    --closest-municipalities (flag, optional): If provided, show the 5 closest
      italian municipalities for each earthquake

    Returns:
        None
    """
    # Create an argument parser object
    parser = argparse.ArgumentParser(
        description="""
        Fetch the strongest earthquakes in Italy within the given
        number of days, based on the given magnitude and count (K).
        """
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
        help="Show the 5 closest ilian municipalities for each earthquake."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Print the parsed arguments (Just to verify the input)
    print(f"""User parameters:
        \n
        Days: {args.days},
        K: {args.K},
        Magnitude: {args.magnitude}
        \n
    """)

    # Create or update the earthquake database
    create_earthquake_db(args.days)

    # Query the database using user inputs
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


# Optional: manual execution
if __name__ == "__main__":
    """
    Manual execution entry point.

    This allows the interface module to be executed directly for development
    and testing purposes. In the final application, the recommended entry point
    is the project-level main.py file.
    """
    main()
