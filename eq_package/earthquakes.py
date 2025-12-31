import requests
import datetime
import json


USGS_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/query?starttime={}&format=geojson&limit=20000'

def get_earthquake(days_past):
    #get the date of today - days_past days at 00 AM
    start_date = (datetime.datetime.now() + datetime.timedelta(days=-days_past)).strftime("%Y-%m-%d")
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