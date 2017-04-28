import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt


def conway_next_world(world):
	# over numpy arrays, for py_func
	world_ = np.zeros_like(world)

	m, n = np.shape(world)
	for i in xrange(1,m):
		for j in xrange(1,n):
			c = np.sum(np.sum(world[i-1:i+2,j-1:j+2])) - world[i,j]

			if world[i,j] == 1:
				world_[i,j] = 1 if c in [2,3] else 0
			else:
				world_[i,j] = 1 if c == 3 else 0

	return world_


def input_fn(shape, batch_size):
	pass


if __name__ == '__main__':

	if True:
		shape = 9,9

		g = tf.Graph()
		with g.as_default():
			m, n = shape

			#worlds = tf.random_uniform([batch_size,m,n],0,2,dtype=tf.int32)
			world = tf.random_uniform([m,n],0,2,dtype=tf.int32)

			world_ = tf.py_func(conway_next_world, [world], tf.int32)

			with tf.Session() as sess:

				world_out, world_out_ = sess.run([world,world_])

		print world_out
		print world_out_
