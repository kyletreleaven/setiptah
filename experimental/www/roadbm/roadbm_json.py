import networkx as nx

import euclidean_roadmap
# import json?

class RoadMatchInstance(object):
	"""Data representation of an instance of Roadmap matching with conversions between JSON and instance tuple.
	"""

	@classmethod
	def from_json(cls, json):
		i = cls()

		roads = json['roads']

		roadmap = nx.MultiDiGraph()
		for road in roads:
			roadmap.add_edge(road['source'], road['target'], key=road['name'], length=road.get('length'))

		i._roadmap = roadmap
		i._source_points = [ (p.get('road'), p.get('coordinate')) for p in json.get('source_points') ]
		i._target_points = [ (p.get('road'), p.get('coordinate')) for p in json.get('target_points') ]

		return i

	def json(self):
		edges = self._roadmap.edges_iter(keys=True, data=True)

		return {
			'roads': [{
				'name': edge,
				'source': i,
				'target': j,
				'length': data.get('length'),
			} for i, j, edge, data in edges ],

			'source_points': [{
				'road': road,
				'coordinate': coord,
			} for (road, coord) in self._source_points ],
			'target_points': [{
				'road': road,
				'coordinate': coord,
			} for (road, coord) in self._target_points ],
		}

	@classmethod
	def from_args(cls, S, T, roadmap):
		i = cls()
		i._source_points = [ p for p in S ]
		i._target_points = [ p for p in T ]
		i._roadmap = nx.MultiDiGraph(roadmap)

		return i

	def source_points(self):
		return [ p for p in self._source_points ]

	def target_points(self):
		return [ p for p in self._target_points ]

	def get_roadmap(self):
		return nx.MultiDiGraph(self._roadmap)




class RoadMatchInstanceEuclidean(object):
	"""Data representation of Euclidean matching instance with conversions between JSON and instance tuple.
	"""

	@classmethod
	def from_json(cls, json):
		i = cls()

		roads = json['roads']
		layout = json['layout']

		roadmap = nx.MultiDiGraph()
		for road in roads:
			roadmap.add_edge(road['source'], road['target'], key=road['name'])

		i._roadmap = roadmap
		i._layout = { rec['vertex']: rec['point'] for rec in layout }
		i._source_points = [ (p.get('road'), p.get('coordinate')) for p in json.get('source_points') ]
		i._target_points = [ (p.get('road'), p.get('coordinate')) for p in json.get('target_points') ]

		return i

	def json(self):
		edges = self._roadmap.edges_iter(keys=True)

		return {
			'roads': [{
				'name': edge,
				'source': i,
				'target': j,
			} for i, j, edge in edges ],

			'layout': [{
				'vertex': u,
				'point': (p[0], p[1]),
			} for u, p in self._layout.iteritems() ],

			'source_points': [{
				'road': road,
				'coordinate': coord,
			} for (road, coord) in self._source_points ],

			'target_points': [{
				'road': road,
				'coordinate': coord,
			} for (road, coord) in self._target_points ],
		}

	@classmethod
	def from_args(cls, S, T, roadmap, layout):
		i = cls()
		i._source_points = [ p for p in S ]
		i._target_points = [ p for p in T ]

		# only keep topology, no data
		i._roadmap = nx.MultiDiGraph()
		for u, v, road in roadmap.edges_iter(keys=True):
			i._roadmap.add_edge(u,v,road)

		i._layout = dict(layout)

		return i

	def source_points(self):
		return [ p for p in self._source_points ]

	def target_points(self):
		return [ p for p in self._target_points ]

	def get_roadmap(self):
		return nx.MultiDiGraph(self._roadmap)

	def get_layout(self):
		return dict(self._layout)
