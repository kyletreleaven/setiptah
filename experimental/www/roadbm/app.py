from flask import Flask
from flask import request

from flask import jsonify

import json
from lxml import etree

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

@app.route('/picture', methods=['GET'])
def my_pretty_picture():
	# create XML 
	root = etree.Element('svg', attrib=dict(width='100', height='100'))

	def make_line(x0,xf, style):
		(x1,y1) = x0
		(x2,y2) = xf
		return etree.Element('line', attrib=dict(
			x1=repr(x1), y1=repr(y1), x2=repr(x2), y2=repr(y2),
			style=style)
		)

	line = make_line((0,0), (50,100), "stroke:rgb(255,0,0);stroke-width:2")
	root.append(line)

	# pretty string
	return etree.tostring(root, pretty_print=True)


@app.route('/igraph', methods=['GET'])
def euclidean_roads_bipartite_match_svg():
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

	print roadmap_.edge
	interval_graph, layout_ = matchvis_util.INTERVAL_GRAPH(match, S, T, roadmap_, layout)

	print layout_

	# turn it into an SVG!
	if False:
		graph_repr = [ '%s -> %s' % (repr(u), repr(v)) for u, v in interval_graph.edges_iter() ]
		other_pos_repr = { repr(u): repr(p) for u, p in layout_.iteritems() }
		return jsonify((graph_repr, other_pos_repr))

	else :
		return draw_interval_graph(interval_graph, layout_, roadmap, layout)


def draw_interval_graph(interval_graph, layout, roadmap, road_layout):
	# we can figure out scaling, etc., later
	# create XML 

	# this needs to be passed in
	width = 800
	height = 600
	root = etree.Element('svg', attrib=dict(width=repr(width), height=repr(height)))

	def make_road(x0,xf):
		(x1,y1) = x0
		(x2,y2) = xf
		return etree.Element('line', attrib=dict(
			x1=repr(x1), y1=repr(y1), x2=repr(x2), y2=repr(y2),
			style='stroke:rgb(0,256,0);stroke-width:1'
			)
		)

	for u, v, in roadmap.edges_iter():
		root.append(make_road(road_layout[u], road_layout[v]))

	def make_match(x0,xf, width):
		(x1,y1) = x0
		(x2,y2) = xf
		return etree.Element('line', attrib=dict(
			x1=repr(x1), y1=repr(y1), x2=repr(x2), y2=repr(y2),
			style='stroke:rgb(0,0,0);stroke-width:%d' % (2 * width)
			)
		)

	def write_X(p):
		x, y = p
		text = etree.Element('text', attrib=dict(
			x=repr(x), y=repr(y), fill='red')
		)
		text.text = 'X'
		return text

	def write_O(p):
		x, y = p
		text = etree.Element('text', attrib=dict(
			x=repr(x), y=repr(y), fill='blue')
		)
		text.text = 'O'
		return text

	for u, v, data in interval_graph.edges_iter(data=True):
		if 'score' not in data: continue
		root.append(make_match(layout[u], layout[v], data.get('score')))

	for u, pos in layout.iteritems():
		type_, _ = u
		if type_ == 'S':
			root.append(write_X(pos))
		elif type_ == 'T':
			root.append(write_O(pos))

	# pretty string
	return etree.tostring(root, pretty_print=True)


if __name__ == "__main__":
	app.run()