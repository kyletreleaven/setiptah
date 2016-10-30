
from collections import deque
import networkx as nx

import pickle


class data: pass

def start_graph(id):
	work = data()

	g = nx.DiGraph()
	g.add_node(id)

	work.GRAPH = g
	work.OPEN = deque([id])
	return work




KYLE = 188052
EMILIO = 114748

FILENAME = 'mathgene.pickle'


if __name__ == '__main__':
	import time
	import numpy as np

	import mathgene

	import argparse
	parser = argparse.ArgumentParser()
	#parser.add_argument('--reset',type=bool,action='store_true')
	parser.add_argument('--reset', action='store_true')
	args = parser.parse_args()

	if args.reset:
		work = start_graph(KYLE)

		with open(FILENAME,'w') as f:
			pickle.dump(work,f)

	else:
		with open(FILENAME, 'r') as f:
			work = pickle.load(f)

		g = work.GRAPH
		OPEN = work.OPEN

		# data structure
		def check_insert(q):
			next_id = q['id']

			#print next_id, OPEN
			#print g.has_node(next_id), next_id in OPEN

			# make sure the node is in the graph
			if g.has_node(next_id): return
			if next_id in OPEN: return

			OPEN.append(next_id)
			#print OPEN

		def save_work(filename):
			# I'm sure there's a more efficient way...
			with open(filename, 'w') as f:
				pickle.dump(work, f)


		while True and len(OPEN) > 0:
			print '%d leaves to OPEN' % len(OPEN)
			id = OPEN.pop()

			try:
				print 'Checking out id=%d' % id
				person = mathgene.download_mathematician(id)
				print 'Found id=%d -> %s' % (id, person['name'])

				g.node[id]['data'] = person

				for q in person['advisors']:
					check_insert(q)
					g.add_edge(q['id'], id)

				if False:
					for q in person['students']:
						check_insert(q)
						g.add_edge(id, q['id'])
					
			except:
				continue


			# Poisson clicks
			delay = np.random.exponential(2)
			print 'Waiting %.2f seconds to avoid suspicion...' % delay
			time.sleep(delay)


