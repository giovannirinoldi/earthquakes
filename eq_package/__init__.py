"""
Earthquake data package.

This package provides utilities to retrieve information about
recent earthquakes using the USGS earthquake service.
"""

from eq_package.earthquakes import gather_earthquakes
from eq_package.earthquakes import create_earthquake_db

__all__ = ["gather_earthquakes", "create_earthquake_db"]