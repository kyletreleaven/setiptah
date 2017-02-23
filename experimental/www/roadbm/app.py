from flask import Flask
from flask import request

from flask import jsonify

import json

# domain
import roadbm_json

import numpy as np

import setiptah.roadbm.bm as bm
from setiptah.roadbm import matchvis_util


app = Flask(__name__)

@app.route('/', methods=['GET'])
def roads_bipartite_match():
	data = { key: value for key, value in request.args.iteritems() }

	query_json = data['query']
	query = json.loads(query_json)

	inst = roadbm_json.RoadMatchInstance.from_json(query)

	S = inst.source_points()
	T = inst.target_points()
	roadmap = inst.get_roadmap()

	match = bm.ROADSBIPARTITEMATCH(S, T, roadmap)

	return jsonify(match)

@app.route('/igraph', methods=['GET'])
def roads_bipartite_match_interval_graph():
	data = { key: value for key, value in request.args.iteritems() }

	query_json = data['query']
	query = json.loads(query_json)

	inst = roadbm_json.RoadMatchInstance.from_json(query)

	S = inst.source_points()
	T = inst.target_points()
	roadmap = inst.get_roadmap()

	match = bm.ROADSBIPARTITEMATCH(S, T, roadmap)

	import random
	# just to see the interface working
	pos = { u: np.array([random.random(), random.random()]) for u in roadmap.nodes_iter() }
	Igraph, other_pos = matchvis_util.INTERVAL_GRAPH(match, S, T, roadmap, pos, length_attr='length')

	graph_repr = [ '%s -> %s' % (repr(u), repr(v)) for u, v in Igraph.edges_iter() ]
	other_pos_repr = { repr(u): repr(p) for u, p in other_pos.iteritems() }
	return jsonify((graph_repr, other_pos_repr))


if __name__ == "__main__":
	app.run()