## An Earthquake data fetching library

This repository contains a file named ```earthquakes.py``` that implements the ```get_earthquake(past_days)``` function. It queries the [USGS](https://earthquake.usgs.gov/fdsnws/event/1/) website to fetch the list of earthquakes registered in the last ```past_days``` days around the world and returns the one with the highest magnitude.
If you run the program, executing the main file with: ```python main.py``` it will  give you results similar to the following: 

```
$ python main.py
The largest earthquake of last 5 days had magnitude 7.7 and was located at 124km NNW of Lucea, Jamaica
```

Note that the project requires the ```json``` and ```requests``` module to run. Note also that USGS limits the maximum number of events returned to 20000, so that it may be useless to query  for events that have an age of more than a few days, as only the lastest 20000 events will be returned.
