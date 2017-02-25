from flask import Flask
from flask import request

from flask import jsonify

import json

# domain
import roadbm_json

import numpy as np

import setiptah.roadbm.bm as bm
from setiptah.roadbm import matchvis_util

import euclidean_roadmap

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

	inst = roadbm_json.RoadMatchInstanceEuclidean.from_json(query)

	S = inst.source_points()
	T = inst.target_points()
	roadmap = inst.get_roadmap()
	layout = inst.get_layout()
	layout = { u: np.array(p) for u, p in layout.iteritems() }

	roadmap_ = euclidean_roadmap.euclidean_roadmap(roadmap, layout)

	match = bm.ROADSBIPARTITEMATCH(S, T, roadmap_)

	interval_graph, layout_ = matchvis_util.INTERVAL_GRAPH(match, S, T, roadmap, layout)

	#print interval_graph.edge
	
	graph_repr = [ '%s -> %s' % (repr(u), repr(v)) for u, v in interval_graph.edges_iter() ]
	other_pos_repr = { repr(u): repr(p) for u, p in layout_.iteritems() }
	return jsonify((graph_repr, other_pos_repr))


if __name__ == "__main__":
	app.run()