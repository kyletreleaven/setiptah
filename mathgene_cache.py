
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
		c.execute('SELECT * FROM mathematicians WHERE Id=?', (id,) )
		row = c.fetchone()

		if row is None:
			# download
			row = mathgene.download_mathematician(id)

			# and write to db!
			def tupform(rec):
				return (rec['id'], rec['name'], rec['degree'], rec['institution'], 
					rec['location'], rec['year'], rec['thesis'])

			tup = tupform(row)
			print tup

			c.execute('INSERT INTO mathematicians VALUES (?,?,?,?,?,?,?)', tup )
			
			# write "edges"
			adviser_edges = [ (a['id'], row['id']) for a in row['advisers'] ]

			print adviser_edges

			c.executemany('INSERT INTO adviserships VALUES (?,?)', adviser_edges)

			student_edges = [ (row['id'], s['id']) for s in row['students'] ]
			c.executemany('INSERT INTO adviserships VALUES (?,?)', student_edges)

			self._conn.commit()

		else:
			KEY_ORDER = ['id', 'name', 'degree', 'institution', 'location', 'year', 'thesis']
			row = dict(zip(KEY_ORDER, row))

			# then, add advisers
			c.execute('SELECT Id,Name FROM adviserships INNER JOIN mathematicians ON Id=AdviserId WHERE StudentId=?', (row['id'],) )
			row['advisers'] = [ dict(zip(['id','name'], tup)) for tup in c.fetchall() ]

			# and students!
			c.execute('SELECT Id,Name FROM adviserships INNER JOIN mathematicians ON Id=StudentId WHERE AdviserId=?', (row['id'],) )
			row['students'] = [ dict(zip(['id','name'], tup)) for tup in c.fetchall() ]

		return row

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

