import argparse
from datetime import datetime
import googlemaps
import os


google_loc = {u'lat': 42.3627572, u'lng': -71.0871087}
home_loc = {u'lat': 42.38427230000001, u'lng': -71.1043136}



def get_key_from_file(filepath):
	with open(filepath,'r') as f:
		api_key = f.read()
	return api_key


def get_client(api_key):
	return googlemaps.Client(key=api_key)


class GeoUtil:
	@staticmethod
	def latlng_obj_to_tup(obj):
		return (obj.get('lat'), obj.get('lng'))

	@staticmethod
	def latlng_tup_to_obj(tup):
		lat, lng = tup
		return dict(lat=lat, lng=lng)


class ClientWrapper:
	def __init__(self, gmaps):
		self._gmaps = gmaps

	def get_query_location(self, query):
		result = self._gmaps.places(query=query)
		first_result = result.get('results')[0]
		loc = first_result.get('geometry').get('location')
		return loc


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--keyfile', type=str)

	args = parser.parse_args()

	api_key = get_key_from_file(args.keyfile)
	gmaps = get_client(api_key)

	# Geocoding an address
	geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

	# Look up an address with reverse geocoding
	reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

	# Request directions via public transit
	now = datetime.now()
	directions_result = gmaps.directions("Sydney Town Hall",
	                                     "Parramatta, NSW",
	                                     mode="transit",
	                                     departure_time=now)

	print directions_result