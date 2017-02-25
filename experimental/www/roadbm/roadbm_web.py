
import random
import json

import numpy as np
import networkx as nx
import requests

import roadbm_json

from setiptah.roadgeometry import generation
from setiptah.roadgeometry import probability


if __name__ == "__main__":

	roadmap = nx.MultiDiGraph()
	roadmap.add_edge(0, 1, 'road1')

	scale = np.array([400,300])
	interchanges = [ scale * np.random.rand(2) for i in xrange(10) ]

	layout = { k: pos for k, pos in enumerate(interchanges) }
	roadmap = generation.DelaunayRoadMap(interchanges)

	distr = probability.UniformDist(roadmap)

	S = [ distr.sample() for k in xrange(20) ]
	T = [ distr.sample() for k in xrange(20) ]

	# shake loose the numpy ints, wtf.
	roadmap_ = nx.MultiDiGraph()
	for u, v, key in roadmap.edges_iter(keys=True):
		roadmap_.add_edge(int(u), int(v), key)
	inst = roadbm_json.RoadMatchInstanceEuclidean.from_args(S, T, roadmap_, layout)

	inst_json = inst.json()

	print json.dumps(inst_json, indent=2)

	request_json = dict(query=json.dumps(inst_json))

	# call the app!
	url = 'http://localhost:5000/igraph'
	res = requests.get(url, params=request_json)

	print res.content
	#match = json.loads(res.content)
	#print match

	#print res.data
