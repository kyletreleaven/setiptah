
#import requests
import json

from collections import namedtuple

def convert(json_value):
	if isinstance(json_value, list):
		return convert_json_list(json_value)
	elif isinstance(json_value, dict):
		return convert_json_dict(json_value)
	else:
		return json_value

def convert_json_list(json_list):
	return map( convert, json_list )

def convert_json_dict(json_dict):
	tuple_class = namedtuple('JsonObject', json_dict.keys() )
	pairs = { k: convert(v) for k, v in json_dict.iteritems() }
	return tuple_class(**pairs)