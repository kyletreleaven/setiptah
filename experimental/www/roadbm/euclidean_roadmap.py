
import numpy as np
import networkx as nx

def euclidean_roadmap(topology, layout):
	result = nx.MultiDiGraph()
	for u, v, road in topology.edges_iter(keys=True):
		road_length = np.linalg.norm( np.array(layout[v]) - np.array(layout[u]) )
		result.add_edge(u, v, road, length=road_length)
	return result

if __name__ == '__main__':

	""" self test """
	topo = nx.MultiDiGraph()
	topo.add_edge(0,1, 'road1')
	topo.add_edge(0,2, 'road2')

	layout = {
		0: (0,0),
		1: (1,0),
		2: (1,1),
	}

	roadmap = euclidean_roadmap(topo, layout)

	print roadmap