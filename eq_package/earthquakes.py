"""
Module for retrieving earthquake data from the USGS API.

The module provides a function to find the strongest earthquake
recorded in the last given number of days.
"""

import requests
import datetime
import json


USGS_URL = ('''https://earthquake.usgs.gov/
            fdsnws/event/1/query?starttime={}&format=geojson&limit=20000''')


def get_earthquake(days_past):
    """
    Return the strongest earthquake recorded in the past given days.

    The function queries the USGS earthquake service starting from
    ``days_past`` days ago and returns the maximum magnitude found
    along with the corresponding location.

    :param days_past: Number of days in the past to search
    :type days_past: int
    :return: Maximum magnitude and its location
    :rtype: tuple
    """
    start_date = (datetime.datetime.now() +
                  datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
    url = USGS_URL.format(start_date)
    r = requests.get(url)
    events = json.loads(requests.get(url).text)
    magnitude = 0
    place = ''
    for event in events['features']:
        try:
            mag = float(event['properties']['mag'])
        except TypeError:
            pass
        if mag > magnitude:
            magnitude = mag
            place = event['properties']['place']

    return magnitude, place
