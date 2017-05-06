import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

# TODO: Train a network to predict CGoL.
# TODO: Write it as a custom Estimator.


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
	m, n = shape

	worlds = tf.random_uniform([batch_size,m,n],0,2,dtype=tf.int32)

	# going to need to shape this...
	callable = lambda w: tf.py_func(conway_next_world, [w], tf.int32, stateful=False)

	worlds_flat = tf.to_float(tf.contrib.layers.flatten(worlds))

	N = np.prod(shape)
	layer1 = tf.contrib.layers.fully_connected(worlds_flat, N, weights_initializer=tf.random_normal_initializer())
	layer2 = tf.contrib.layers.fully_connected(layer1, N, weights_initializer=tf.random_normal_initializer())

	logits = tf.reshape(layer2, [-1] + shape)

	# TODO: Use loss for logistic regression.
	target_next_worlds = tf.map_fn(callable, worlds)

	loss = tf.losses.sigmoid_cross_entropy(
		target_next_worlds,
		logits)

	worlds_ = tf.sigmoid(logits)

	return worlds, worlds_, layer1, layer2, logits, loss


if __name__ == '__main__':

	shape = 9,9
	m, n = shape

	if False:
		g = tf.Graph()
		with g.as_default():

			#worlds = tf.random_uniform([batch_size,m,n],0,2,dtype=tf.int32)
			world = tf.random_uniform([m,n],0,2,dtype=tf.int32)

			world_ = tf.py_func(conway_next_world, [world], tf.int32)

			with tf.Session() as sess:

				world_out, world_out_ = sess.run([world,world_])

		print world_out
		print world_out_


	if True:
		g = tf.Graph()
		with g.as_default():

			worlds, worlds_, layer1, layer2, logits, loss = input_fn([2,4], 20)

			with tf.Session() as sess:
				sess.run(tf.global_variables_initializer())

				opt = tf.train.AdagradOptimizer(learning_rate=0.001)
				
				for k in xrange(100):
					print k
					opt.minimize(loss)

				# get samples after learning				
				res_out = sess.run([worlds,worlds_])

				#worlds_out, worlds_out_ = sess.run([worlds,worlds_])

