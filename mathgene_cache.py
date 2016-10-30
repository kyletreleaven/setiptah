
# apparently, no more pickle, great!
import pickle

import networkx as nx

import mathgene


class MiniCache:
	def get_mathematician(self, id):
		return mathgene.download_mathematician(id)


class Cache:
	def __init__(self, filename):
		self._filename = filename

		try:
			self._read_graph()
		except:
			self._graph = nx.DiGraph()
			self._write_graph()

	def _read_graph(self):
		with open(self._filename,'r') as f:
			self._graph = pickle.load(f)

	def _write_graph(self):
		with open(self._filename,'w') as f:
			pickle.dump(self._graph, f)

	def get_mathematician(self, id):
		if self._graph.has_node(id):
			person = self._graph.node[id]['data']

		else:
			person = mathgene.download_mathematician(id)
			self._graph.add_node(id)
			self._graph.node[id]['data'] = person

			self._write_graph()
