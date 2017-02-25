
import unittest
import networkx as nx

import roadbm_json

class TestRoadmapMatchingJson(unittest.TestCase):

	def testEuclideanJson(self):

		S = []
		T = []
		roadmap = nx.MultiDiGraph()
		roadmap.add_edge(0,1, 'A')
		layout = { 0: (0,0), 1: (1,0) }

		inst = roadbm_json.RoadMatchInstanceEuclidean.from_args(S, T, roadmap, layout)

		inst_json = inst.json()

		inst_ = roadbm_json.RoadMatchInstanceEuclidean.from_json(inst_json)

		S_ = inst_.source_points()
		T_ = inst_.target_points()

		self.assertSetEqual(set(S), set(S_))
		self.assertSetEqual(set(T), set(T_))

		layout_ = inst_.get_layout()
		self.assertEqual(layout[0], layout_[0])
		self.assertEqual(layout[1], layout_[1])


if __name__ == '__main__':
	unittest.main()