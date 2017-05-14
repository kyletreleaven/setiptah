import os
from six.moves import urllib
import sys
import tarfile

import tensorflow as tf
from tensorflow.python.platform import gfile

# update?


def maybe_download_and_extract(data_url, dest_directory, force_download=False):

	if not os.path.exists(dest_directory):
		os.makedirs(dest_directory)

	filename = data_url.split('/')[-1]
	filepath = os.path.join(dest_directory, filename)

	if force_download or not os.path.exists(filepath):
	
		def _progress(count, block_size, total_size):
			sys.stdout.write('\r>> Downloading %s %.1f%%' %
				(filename,
					float(count * block_size) / float(total_size) * 100.0))

			sys.stdout.flush()

		filepath, _ = urllib.request.urlretrieve(data_url, filepath, _progress)

		print()
		statinfo = os.stat(filepath)
		print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')

	tarfile.open(filepath, 'r:gz').extractall(dest_directory)


def import_graph_from_file(model_filename):
	with gfile.FastGFile(model_filename, 'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		tf.import_graph_def(graph_def) #, name='', return_element=[])




if __name__ == '__main__':
	"""
	After you run this:
	
	tensorboard --logdir=/tmp/stuff/summaries (or whatever SUMMARIES_DIR is set to)
	"""

	DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
	#DATA_URL = 'http://download.tensorflow.org/models/image/imagenet/inception-2015-12-05.tgz'
	MODEL_DIR = '/tmp/stuff'

	SUMMARIES_DIR = '/tmp/stuff/summaries'

	if gfile.Exists(SUMMARIES_DIR):
		gfile.DeleteRecursively(SUMMARIES_DIR)
	gfile.MakeDirs(SUMMARIES_DIR)


	maybe_download_and_extract(DATA_URL, MODEL_DIR)

	graph_filename = os.path.join(MODEL_DIR, 'classify_image_graph_def.pb')

	g = tf.Graph()
	with g.as_default():
		with tf.Session() as sess:
			import_graph_from_file(graph_filename)

			merged = tf.summary.merge_all()
			train_writer = tf.summary.FileWriter(SUMMARIES_DIR + '/train', g)

			init = tf.global_variables_initializer()
			sess.run(init)

			train_summary, = sess.run([merged])
			train_writer.add_summary(train_summary, 0)	# change to global step?