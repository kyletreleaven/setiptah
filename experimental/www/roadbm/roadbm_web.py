
import random
import json

import networkx as nx
import requests

import roadbm_json


if __name__ == "__main__":

	roadmap = nx.MultiDiGraph()
	roadmap.add_edge(0, 1, 'road1')

	layout = {
		0: (0,0),
		1: (100,100),
		2: (0,100),
		3: (100,0),
	}

	S = [ ('road1', random.random()) for k in xrange(10) ]
	T = [ ('road1', random.random()) for k in xrange(10) ]

	inst = roadbm_json.RoadMatchInstanceEuclidean.from_args(S, T, roadmap, layout)

	inst_json = inst.json()

	request_json = dict(query=json.dumps(inst_json))

	# call the app!
	url = 'http://localhost:5000/igraph'
	res = requests.get(url, params=request_json)

	print res.content
	#match = json.loads(res.content)
	#print match

	#print res.data
