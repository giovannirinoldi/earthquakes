from eq_package.earthquakes import get_earthquake

days = 10
mag, place = get_earthquake(days)

print("The largest earthquake of last {} days had magnitude {} and was located at {}".format(days, mag, place))