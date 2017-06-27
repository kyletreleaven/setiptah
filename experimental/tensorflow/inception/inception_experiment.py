
# https://www.tensorflow.org/extend/estimators
# https://github.com/tensorflow/tensorflow/tree/master/tensorflow/examples/image_retraining
# https://research.googleblog.com/2016/03/train-your-own-image-classifier-with.html
# https://github.com/tensorflow/models/blob/master/inception/README.md#how-to-train-from-scratch

import graph_utils
import numpy as np
import os
import tensorflow as tf
from tensorflow.contrib.slim.python.slim.nets import inception_v3
from tensorflow.python.platform import gfile

IMAGE_SIZE=[299,299]
IMAGE_CHANNELS=3

NUM_CLASSES=120


def get_model_fn():

  def model_fn(image_batch, labels, mode, params=None):

    image_batch = tf.to_float(image_batch)
    labels = tf.to_float(labels)

    predictions, inception_layers_dict = inception_v3.inception_v3(
      image_batch,
      num_classes=120,
      is_training=True,
      )

    loss = tf.losses.log_loss(labels,predictions)

    if mode == tf.contrib.learn.ModeKeys.TRAIN:
      graph_vars = graph_utils.get_grouped_trainable_variables()
      optimizer = tf.train.AdagradOptimizer(learning_rate=0.0001)
      var_list = list(graph_vars.get_all_vars())
      train_op = optimizer.minimize(loss, var_list=var_list)

      return tf.contrib.learn.ModelFnOps(mode, loss=loss, train_op=train_op)

    elif mode == tf.contrib.learn.ModeKeys.EVAL:
      # TODO(ktreleav): This mode is not quite right.
      return tf.contrib.learn.ModelFnOps(mode, loss=loss, eval_metric_ops={
        'loss': loss
        })

    elif mode == tf.contrib.learn.ModeKeys.INFER:
      return tf.contrib.learn.ModelFnOps(mode, predictions = predictions)

    else:
      raise Exception()

  return model_fn


def input_fn():
  inputs_shape = [None] + IMAGE_SIZE + [IMAGE_CHANNELS]
  image_batch_placeholder = tf.placeholder(tf.float32, shape=inputs_shape)
  
  # or is this one-hot already?
  labels_placeholder = tf.placeholder(tf.int32, shape=[None,1])

  return image_batch_placeholder, labels_placeholder

def get_estimator():
  # https://www.tensorflow.org/api_docs/python/tf/contrib/learn/Estimator
  pass



if __name__ == '__main__':
  model_fn = get_model_fn()
  estimator = tf.contrib.learn.Estimator(model_fn=model_fn)

  image_batch = np.zeros([1]+IMAGE_SIZE+[IMAGE_CHANNELS])

  INT_LABELED_NOT_ONE_HOT = False
  if INT_LABELED_NOT_ONE_HOT:
    labels = [0] * 1
  else:
    labels = np.zeros([1,NUM_CLASSES])
    labels[0] = 1.0

  if True:
    estimator.fit(image_batch, labels, steps=1)

  if True:
    y = estimator.predict(image_batch)


  if False:
    summaries_dir = '/tmp/stuff/summaries'
    if gfile.Exists(summaries_dir):
      gfile.DeleteRecursively(summaries_dir)
    gfile.MakeDirs(summaries_dir)

    g = tf.Graph()
    with g.as_default():

      inputs, labels = input_fn()

      model_fn = get_model_fn()

      model_stuff, gvs = model_fn(inputs, labels, None, None)

      with tf.Session() as sess:

        merged = tf.summary.merge_all()
        train_writer = tf.summary.FileWriter(summaries_dir + '/train', g)

        init = tf.global_variables_initializer()
        sess.run(init)

        train_summary, = sess.run([merged])
        train_writer.add_summary(train_summary, 0)  # change to global step?


