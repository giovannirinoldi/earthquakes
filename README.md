# 🌍 Italian Earthquake Tracker

A Python application that fetches, stores, and analyzes real-time earthquake data from Italy using the INGV (Istituto Nazionale di Geofisica e Vulcanologia) API. The application provides advanced filtering, SQLite storage, and optional geographic proximity analysis to Italian municipalities.

## 📋 Features

- **Real-time Data Fetching**: Retrieves earthquake data from the official INGV API
- **Geographic Filtering**: Automatically filters earthquakes within Italy's bounding box
- **SQLite Database**: Persistent storage with automatic duplicate prevention
- **Advanced Querying**: Filter by magnitude, time range, and number of results
- **Proximity Analysis**: Calculate and display the 5 closest Italian municipalities to each earthquake epicenter
- **Haversine Distance Calculation**: Accurate distance measurements using the spherical Earth model
- **Comprehensive Testing**: Full test suite with unittest framework

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Dependencies

Install the required packages:

```bash
pip install requests
```

The following standard library modules are also used:
- `sqlite3`
- `csv`
- `argparse`
- `datetime`
- `math`
- `unittest`

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd earthquakes
   ```
3. Ensure all files are present:
   - `main.py`
   - `eq_package/earthquakes.py`
   - `eq_package/bounding_box.csv`
   - `italian_municipalities.csv`
   - `test_project.py`

## 💻 Usage

### Basic Command

Fetch the top K strongest earthquakes from the last N days with a minimum magnitude:

```bash
python main.py --days <DAYS> --K <COUNT> --magnitude <MIN_MAG>
```

### With Municipality Proximity

Add the `--closest-municipalities` flag to show the 5 nearest Italian cities to each earthquake:

```bash
python main.py --days <DAYS> --K <COUNT> --magnitude <MIN_MAG> --closest-municipalities
```

### Examples

**Example 1**: Get the top 5 earthquakes from the last 30 days with magnitude ≥ 2.0
```bash
python main.py --days 30 --K 5 --magnitude 2.0
```

**Output**:
```
day: 2026-01-10, time: 04:53:11, magnitude: 5.1, lat: 37.7492, lon: 16.2262, place: Costa Calabra sud-orientale (Reggio di Calabria)
day: 2025-12-17, time: 22:07:46, magnitude: 4.2, lat: 42.5563, lon: 17.619, place: Costa Croata meridionale (CROAZIA)
day: 2025-12-15, time: 09:11:22, magnitude: 4.0, lat: 36.4612, lon: 16.7235, place: Mar Ionio Meridionale (MARE)
...
```

**Example 2**: Same query with closest municipalities
```bash
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

### Command-Line Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `--days` | int | Yes | Number of days in the past to fetch earthquake data |
| `--K` | int | Yes | Maximum number of strongest earthquakes to return |
| `--magnitude` | float | Yes | Minimum magnitude threshold for filtering |
| `--closest-municipalities` | flag | No | Show 5 closest Italian municipalities for each earthquake |

## 📁 Project Structure

```
earthquakes/
│
├── main.py                          # Main entry point and CLI interface
├── eq_package/
│   ├── __init__.py                  # Package initializer
│   ├── earthquakes.py               # Core functionality (API, database, calculations)
│   ├── bounding_box.csv             # Italy's geographic bounding box
│   ├── LICENSE                      # Package license
│   ├── README.md                    # Package documentation
│   └── write_boundingbox.py         # Utility for bounding box generation
│
├── italian_municipalities.csv       # Dataset of 170+ Italian municipalities with coordinates
├── test_project.py                  # Comprehensive test suite
├── earthquakes.db                   # SQLite database (auto-generated)
└── README.md                        # This file
```

## 🔧 Core Functions

### `gather_earthquakes(days)`
Fetches earthquake data from the INGV API within Italy's bounding box for the specified time range.

**Returns**: List of tuples `(day, time, magnitude, latitude, longitude, place)`

### `create_earthquake_db(days)`
Creates/updates an SQLite database with earthquake records, automatically handling duplicates.

### `query_db(k, days, min_magnitude)`
Queries the database for the top K earthquakes matching the criteria, sorted by decreasing magnitude.

**Returns**: List of earthquake tuples

### `calculate_distance(lat1, lon1, lat2, lon2)`
Calculates the great-circle distance between two points using the Haversine formula.

**Returns**: Distance in kilometers

### `get_closest_municipalities(eq_lat, eq_lon, n=5)`
Finds the N closest Italian municipalities to an earthquake epicenter.

**Returns**: List of tuples `(municipality_name, distance_km)`

### `print_earthquakes(earthquakes)`
Prints earthquake records in a standardized format.

## 🧪 Testing

The project includes a comprehensive test suite with 4 test cases:

```bash
python -m unittest test_project.py
```

### Test Cases

1. **test_bounding_box**: Verifies that Italian cities (Padova, Parma, Palermo) are within the defined bounding box
2. **test_magnitude**: Ensures no earthquake exceeds the physical maximum of 9.5
3. **test_order**: Confirms query results are sorted by decreasing magnitude
4. **test_database_has_data**: Validates that the database contains earthquake records

### Running Tests with Verbose Output

```bash
python -m unittest test_project.py -v
```

## 📊 Data Sources

- **Earthquake Data**: [INGV (Istituto Nazionale di Geofisica e Vulcanologia)](https://webservices.ingv.it/)
  - Real-time seismic data from Italy's national geophysical institute
  - API endpoint: `https://webservices.ingv.it/fdsnws/event/1/query`

- **Municipality Coordinates**: `italian_municipalities.csv`
  - 170+ major Italian municipalities
  - Includes name, latitude, and longitude for each location

- **Geographic Boundaries**: `eq_package/bounding_box.csv`
  - Italy's bounding box: 35°N - 47.5°N, 5°E - 20°E

## 🛠️ Technical Details

### Database Schema

**Table**: `earthquakes_db`

| Column | Type | Description |
|--------|------|-------------|
| day | TEXT | Date in YYYY-MM-DD format |
| time | TEXT | Time in HH:MM:SS format (UTC) |
| mag | REAL | Earthquake magnitude |
| latitude | REAL | Epicenter latitude |
| longitude | REAL | Epicenter longitude |
| place | TEXT | Human-readable location description |

**Constraints**: UNIQUE on all columns to prevent duplicates

### Haversine Formula

The distance calculation uses the Haversine formula for great-circle distances:

```
a = sin²(Δlat/2) + cos(lat1) × cos(lat2) × sin²(Δlon/2)
c = 2 × atan2(√a, √(1-a))
distance = R × c
```

Where R = 6371 km (Earth's radius)

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is developed for educational purposes as part of the Lab of Software Project Development course at H-FARM.

## ⚠️ Disclaimer

This application is for educational and informational purposes only. For official earthquake information and emergency situations, please refer to:
- [INGV Official Website](https://www.ingv.it/)
- Local civil protection authorities
- Emergency services (112 in Italy)

## 📧 Support

For questions, issues, or suggestions, please open an issue in the repository.

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Python Version**: 3.8+
