import argparse

from eq_package.earthquakes import *


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

    # Parse the arguments
    args = parser.parse_args()

    # Print the parsed arguments (For now, just to verify the input)
    #print(f"Days: {args.days}, K: {args.K}, Magnitude: {args.magnitude}")

    create_earthquake_db(args.days)

    # Call query_db with user inputs
    earthquakes = query_db(args.K, args.days, args.magnitude)

    # Print the results in the required format
    print_earthquakes(earthquakes)

if __name__ == "__main__":
    main()

