
# apparently, no more pickle, great!
import pickle
import sqlite3


import networkx as nx

import mathgene


class MiniCache:
	def get_mathematician(self, id):
		return mathgene.download_mathematician(id)


class SQLiteCache:
	def __init__(self, filename):
		self._conn = sqlite3.connect(filename)

	def get_mathematician(self, id):
		c = self._conn.cursor()

		from mathgene_db import MathgeneCursor
		superc = MathgeneCursor(c)

		mathn = superc.fetch_mathematician(id)

		if mathn is None:
			# then download...
			print 'downloading %d from internet' % id
			mathn = mathgene.download_mathematician(id)

			# and write to db!
			superc.insert_mathematician(mathn)
			self._conn.commit()

		else:
			print 'found in local cache'

		return mathn

	def __del__(self):
		self._conn.close()


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

