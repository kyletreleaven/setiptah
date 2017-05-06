import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

# Very frustrating. This is practically identical to example code, but does not converge.

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
	res = dict()

	m, n = shape

	# don't worry about batch approach for now...
	#worlds = tf.random_uniform([batch_size,m,n],0,2,dtype=tf.int32)
	world = tf.random_uniform([m,n],0,2,dtype=tf.int32)
	next_world = tf.py_func(conway_next_world, [world], tf.int32, stateful=False)

	res['input'] = world, next_world

	# going to need to shape this...
	#callable = lambda w: tf.py_func(conway_next_world, [w], tf.int32, stateful=False)

	# TODO: Use loss for logistic regression.
	#target_next_worlds = tf.map_fn(callable, worlds)

	#world_flat = tf.to_float(tf.contrib.layers.flatten(world))

	# The first dimension is because layers treat data in batches, i.e., [batch_size==1,-1]
	input_layer = tf.to_float(tf.reshape(world,[1,-1]))

	N = np.prod(shape)
	layer1 = tf.contrib.layers.fully_connected(input_layer, N)
	#weights_initializer=tf.random_normal_initializer())
	layer2 = tf.contrib.layers.fully_connected(layer1, N)
	#weights_initializer=tf.random_normal_initializer())
	
	# next world statistics
	res['output'] = outputs = dict()

	if True:
		layer3 = tf.contrib.layers.fully_connected(layer2, N,
			activation_fn=tf.nn.sigmoid)

		next_world_probabilities = tf.reshape(layer3, shape)

	else:
		layer3 = tf.contrib.layers.fully_connected(layer2, N, activation_fn=None) # stay linear
		logits = tf.reshape(layer3, shape)

		outputs['logits'] = logits

		next_world_probabilities = tf.sigmoid(logits)

	next_world_prediction = tf.to_int32(tf.greater(next_world_probabilities,.5))

	outputs['next_world_probabilities'] = next_world_probabilities
	outputs['next_world_prediction'] = next_world_prediction

	#loss = tf.losses.sigmoid_cross_entropy(next_world, logits)
	#loss = tf.losses.log_loss(next_world, next_world_probabilities)
	loss = tf.losses.log_loss(next_world_probabilities, next_world)
	res['loss'] = loss

	return res


if __name__ == '__main__':

	shape = 5,5
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
		losses = []

		g = tf.Graph()
		with g.as_default():

			ops = input_fn(shape, None) # no batch size currently

			loss = ops.get('loss')
			optimizer = tf.train.AdagradOptimizer(1.0)
			train = optimizer.minimize(loss)

			with tf.Session() as sess:
				sess.run(tf.global_variables_initializer())

				for k in xrange(10000):
					_, loss_out = sess.run([train, loss])

					if k % 100 == 0 :
						print k, loss_out
						losses.append(loss_out)

				# get samples after learning
				world_op, _ = ops['input']
				next_world_prediction_op = ops['output'].get('next_world_prediction')

				for k in xrange(20):
					world, next_world_predicted = sess.run([world_op, next_world_prediction_op])

					next_world = conway_next_world(world)

					print np.sum(np.sum(np.abs(next_world-next_world_predicted)))

		import matplotlib.pyplot as plt
		plt.plot(range(len(losses)), losses)
		plt.show()

		# TODO(ktreleav): Save/load the model.
