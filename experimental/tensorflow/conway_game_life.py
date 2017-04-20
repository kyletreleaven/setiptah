import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt

def f(x):
	return np.sin(x)


def get_feature_columns():
	patch = tf.something.real_valued_column("patch", dimension=9)
	return [patch]


def input_fn():
	xs = tf.random_uniform([100], -np.pi, np.pi)
	ys = tf.py_func(f, [xs], tf.float32)

	return {"xs": xs}, ys


if __name__ == '__main__':

	"""
		estimator = tf.learn.contrib.DNNClassifier(
    feature_columns=[sparse_feature_a_emb, sparse_feature_b_emb],
    hidden_units=[1024, 512, 256])
	"""

	if True:
		graph = tf.Graph()
		with graph.as_default():

			input_data, ys = input_fn()

			with tf.Session() as sess:
				sess.run(tf.initialize_all_variables())
				input_data_out, ys_out = sess.run([input_data, ys])
				
		print input_data_out, ys_out
		plt.scatter(input_data_out["xs"], ys_out)
		plt.show()
