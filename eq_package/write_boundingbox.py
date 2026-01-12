"""
This module provides functionality to write a dictionary containing geographic
bounding box data to a CSV file. The bounding box specifies the geographic
area of interest using minimum/maximum latitude and longitude values.

The generated CSV file is saved in the 'data' directory and can be used as input
for other programs or functions that require bounding box information, such as
querying earthquake data from APIs.
"""

import csv
import pathlib


def write_bounding_box():
    """
    Writes the geographic bounding box data to a CSV file.

    The bounding box data includes the following values:
    - Minimum latitude
    - Maximum latitude
    - Minimum longitude
    - Maximum longitude

    Each key-value pair from the bounding box dictionary is written as a row
    in the file 'bounding_box.csv', with the key in the first column and the
    corresponding value in the second column.

    File Created:
        - bounding_box.csv: Contains rows formatted as:
          key, value

    Returns:
        None: The function does not return a value; it writes output directly
        to a file.
    """
    # Define the bounding box dictionary
    bounding_box = {
        'minlatitude': 35.0,
        'maxlatitude': 47.5,
        'minlongitude': 5.0,
        'maxlongitude': 20.0
    }

    # Resolve path to data directory
    csv_path = pathlib.Path(__file__).resolve().parent.parent / "data" / "bounding_box.csv"

    # Open csv_path in write mode
    # Use newline='' to prevent extra blank lines in the CSV file on Windows
    with open(csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)  # Initialize the CSV writer
        # Write each key-value pair as a row in the CSV file
        for key, value in bounding_box.items():
            writer.writerow([key, value])


# Call the function to create and write to the CSV file if this script is executed
if __name__ == "__main__":
    write_bounding_box()