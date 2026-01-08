import csv

def write_bounding_box():
    # Define the bounding box dictionary
    bounding_box = {
        'minlatitude': 35.0,
        'maxlatitude': 47.5,
        'minlongitude': 5.0,
        'maxlongitude': 20.0
    }

    # Write the dictionary to a CSV file
    with open('bounding_box.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the keys and values as rows
        for key, value in bounding_box.items():
            writer.writerow([key, value])

# Call the function to write the file
if __name__ == "__main__":
    write_bounding_box()