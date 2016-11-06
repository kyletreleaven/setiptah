
from collections import deque
import networkx as nx

#import matplotlib.pyplot as plt

class data: pass

def start_graph(id):
	work = data()

	g = nx.DiGraph()
	g.add_node(id)

	work.GRAPH = g
	work.OPEN = deque([id])
	return work


if __name__ == '__main__':
	import argparse
	import pickle

	import sqlite3 as db
	import mathgene_db

	parser = argparse.ArgumentParser()
	#parser.add_argument('--reset',type=bool,action='store_true')
	parser.add_argument('db', type=str)
	args = parser.parse_args()

	conn = db.connect(args.db)

	c = conn.cursor()
	superc = mathgene_db.MathgeneCursor(c)

	graph = superc.fetch_graph()

	#nx.draw(graph)
	#plt.show()




