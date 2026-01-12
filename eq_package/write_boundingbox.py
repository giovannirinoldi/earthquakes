"""
Bounding box utilities for the Earthquakes project.

This module provides functionality to write the geographic bounding box
parameters to a CSV file. The bounding box defines the geographic area of
interest (Italy) using minimum and maximum latitude and longitude values.

The generated CSV file is used by other modules (e.g. ingv_client) to restrict
earthquake queries to the Italian territory.

Output file:
    data/bounding_box.csv

File format:
    Each row contains a key-value pair:
        <key>,<value>
    where key is one of:
        - minlatitude
        - maxlatitude
        - minlongitude
        - maxlongitude
"""

import csv
import pathlib

def write_bounding_box():
    """
    Write the geographic bounding box data to a CSV file.

    The bounding box is defined by the following values:
        - minlatitude
        - maxlatitude
        - minlongitude
        - maxlongitude

    These values are written as key-value pairs into the file:
        data/bounding_box.csv

    Returns:
        None
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


# Optional: Test the function
if __name__ == "__main__":
    """
    Manual test block.

    When this module is executed directly, it will generate the bounding_box.csv
    file in the data directory using the predefined bounding box values.

    This is intended for development and debugging purposes only.
    """
    write_bounding_box()