import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

def f(x):
	return np.sin(x)


def get_feature_columns():
	patch = tf.something.real_valued_column("patch", dimension=9)
	return [patch]


def input_fn():
	xs = tf.random_uniform([100,1], -np.pi, np.pi)
	
	ys = tf.py_func(f, [xs], tf.float32)

	# need to shape the output of py_func
	rows = tf.shape(ys)[0]
	ys = tf.reshape(ys, [rows,1])
	
	return {"xs": xs}, ys


if __name__ == '__main__':

	"""
		estimator = tf.learn.contrib.DNNClassifier(
    feature_columns=[sparse_feature_a_emb, sparse_feature_b_emb],
    hidden_units=[1024, 512, 256])
	"""
	#optimizer = tf.train.ProximalAdagradOptimizer(learning_rate=0.1,l1_regularization_strength=0.001)

	if True:
		feature_column = tf.contrib.layers.real_valued_column("xs")
		
		estimator = tf.contrib.learn.DNNRegressor(
			feature_columns=[feature_column],
			hidden_units=[32,16,4])

		estimator.fit(input_fn=input_fn, steps=10000)

		xs_in = -np.pi + 2 * np.pi * np.random.random(50)

		#ys_out = estimator.predict({"xs": xs_in})

		xs = np.linspace(-np.pi,np.pi,100)
		ys_f = f(xs)

		ys_model = [ y for y in estimator.predict({"xs": xs}) ]

		#plt.scatter(xs_in, [y for y in ys_out])
		plt.plot(xs, ys_f, c='b')
		plt.plot(xs, ys_model, c='r')
		plt.show()
		#estimator.predict(input_fn=input_fn)


	if False:
		graph = tf.Graph()
		with graph.as_default():

			input_data, ys = input_fn()

			print ys.get_shape()

			with tf.Session() as sess:
				sess.run(tf.initialize_all_variables())
				input_data_out, ys_out = sess.run([input_data, ys])
				
		#print input_data_out, ys_out
		plt.scatter(input_data_out["xs"], ys_out)
		plt.show()
