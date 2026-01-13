# Italian Earthquake Tracker

This project is a command-line application that retrieves recent earthquake data
from the INGV (Istituto Nazionale di Geofisica e Vulcanologia) web services,
stores them in a local SQLite database, and allows the user to query the strongest
earthquakes in Italy within a given time window and magnitude threshold.

The project was developed for educational purposes as part of the
Lab of Software Project Development course at H-FARM.

## Features

- Retrieval of earthquake data from the INGV API
- Geographic filtering using a predefined bounding box
- Persistent storage using SQLite with duplicate prevention
- Querying by time window, magnitude and number of results
- Computation of distances to the closest Italian municipalities
- Automated test suite using the unittest framework

## Project Structure

```
earthquakes/
│
├── data/
│   ├── bounding_box.csv              # Italy’s geographic bounding box (auto-generated)
│   ├── italian_municipalities.csv    # Dataset of Italian municipalities with coordinates
│   └── earthquakes.db                # SQLite database (auto-generated)
│
├── eq_package/
│   ├── __init__.py
│   ├── interface.py                  # Command-line interface (argparse)
│   ├── ingv_client.py                # INGV API client
│   ├── db.py                         # Database creation and querying
│   ├── municipalities.py             # Distance and proximity utilities
│   └── write_boundingbox.py          # Bounding box generator
│
├── tests/
│   └── test_project.py               # Unit test suite
│
├── main.py                           # Project entry point
├── README.md                         # This file
└── LICENSE                           # License file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Dependencies

Install the required packages:

```
pip install requests
```

The following standard library modules are also used:
- `sqlite3`
- `csv`
- `argparse`
- `datetime`
- `math`
- `unittest`
- `pathlib`

### Setup

1. Clone or download this repository
2. Navigate to the project directory:

   ```
   cd earthquakes
   ```
The files `data/bounding_box.csv` and `data/earthquakes.db` are automatically generated when the application is first executed.

## Usage

### Basic Command

Fetch the top K strongest earthquakes from the last N days with a minimum magnitude:

```
python main.py --days <DAYS> --K <COUNT> --magnitude <MIN_MAG>
```

### With Municipality Proximity

Add the `--closest-municipalities` flag to show the 5 nearest Italian cities to each earthquake:

```
python main.py --days <DAYS> --K <COUNT> --magnitude <MIN_MAG> --closest-municipalities
```

### Examples

**Example 1**: Get the top 5 earthquakes from the last 30 days with magnitude ≥ 2.0
```
python main.py --days 30 --K 5 --magnitude 2.0
```

**Output**:
```
day: 2026-01-10, time: 04:53:11, magnitude: 5.1, lat: 37.7492, lon: 16.2262, place: Costa Calabra sud-orientale (Reggio di Calabria)
day: 2026-01-13, time: 08:27:58, magnitude: 4.3, lat: 44.3162, lon: 11.9993, place: 7 km SW Russi (RA)
day: 2025-12-17, time: 22:07:46, magnitude: 4.2, lat: 42.5563, lon: 17.619, place: Costa Croata meridionale (CROAZIA)
day: 2026-01-13, time: 08:29:17, magnitude: 4.1, lat: 44.288, lon: 11.9795, place: 8 km E Faenza (RA)
day: 2025-12-15, time: 09:11:22, magnitude: 4.0, lat: 36.4612, lon: 16.7235, place: Mar Ionio Meridionale (MARE)
```

**Example 2**: Same query with closest municipalities
```
python main.py --days 30 --K 5 --magnitude 2.0 --closest-municipalities
```

**Output**:
```
day: 2026-01-10, time: 04:53:11, magnitude: 5.1, lat: 37.7492, lon: 16.2262, place: Costa Calabra sud-orientale (Reggio di Calabria)
  - Reggio Calabria: 64.86 km
  - Messina: 76.91 km
  - Acireale: 94.58 km
  - Barcellona Pozzo di Gotto: 99.17 km
  - Vibo Valentia: 103.61 km
...
```

### Available Command-Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--days` | int | Yes | Number of days in the past to fetch earthquake data |
| `--K` | int | Yes | Maximum number of strongest earthquakes to return |
| `--magnitude` | float | Yes | Minimum magnitude threshold for filtering |
| `--closest-municipalities` | flag | No | Show 5 closest Italian municipalities for each earthquake |

## Testing

The project includes a test suite implementing the required test cases:

```
python -m unittest tests/test_project.py
```

### Test Cases

1. **test_bounding_box**: Verifies that Italian cities (Padova, Parma, Palermo) are within the defined bounding box
2. **test_magnitude**: Ensures no earthquake exceeds the physical maximum of 9.5
3. **test_order**: Confirms query results are sorted by decreasing magnitude
4. **test_database_has_data**: Validates that the database contains earthquake records

### Running Tests with Verbose Output

```
python -m unittest tests/test_project.py -v
```

-v prints each test name and its result (ok/fail/error) for easier debugging.

## Data Sources

- **Earthquake Data**: [INGV (Istituto Nazionale di Geofisica e Vulcanologia)](https://webservices.ingv.it/)
  - Real-time seismic data from Italy's national geophysical institute
  - API endpoint: `https://webservices.ingv.it/fdsnws/event/1/query`

- **Municipality Coordinates**: `data/italian_municipalities.csv`
  - 170+ major Italian municipalities
  - Includes name, latitude, and longitude for each location

- **Geographic Boundaries**: `data/bounding_box.csv`
  - Italy's bounding box: 35°N - 47.5°N, 5°E - 20°E
  - Auto-generated if missing

## Technical Details

### Database Schema

**Table**: `earthquakes_db`

| Column | Type | Description |
|--------|------|-------------|
| day | TEXT | Date in YYYY-MM-DD format |
| time | TEXT | Time in HH:MM:SS format (UTC, as provided by INGV) |
| mag | REAL | Earthquake magnitude |
| latitude | REAL | Epicenter latitude |
| longitude | REAL | Epicenter longitude |
| place | TEXT | Human-readable location description |

**Constraints**: A UNIQUE constraint is applied to all columns to prevent duplicate earthquake records when the database is updated multiple times.

### Haversine Formula

The distance calculation uses the Haversine formula for great-circle distances:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1-a))
distance = R × c
```

Where R = 6371 km (Earth's radius)

## License

This project is released under the Apache License, Version 2.0.  
See the LICENSE file for details.

## Disclaimer

This application is for educational and informational purposes only. For official earthquake information and emergency situations, please refer to:
- [INGV Official Website](https://www.ingv.it/)
- Local civil protection authorities
- Emergency services (112 in Italy)

## Support

For questions, issues, or suggestions, please open an issue in the repository.

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Python Version**: 3.8+