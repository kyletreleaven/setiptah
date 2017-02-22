import networkx as nx

# import json?

class RoadMatchInstance(object):

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

