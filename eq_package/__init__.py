"""
Earthquake data package.

This package provides utilities to retrieve information about
recent earthquakes using the USGS earthquake service.
"""

from eq_package.earthquakes import get_earthquake

__all__ = ["get_earthquake"]