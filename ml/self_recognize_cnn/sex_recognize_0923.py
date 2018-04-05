#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 03:08:48 2017
@author: root
"""

import tensorflow as tf
import numpy, pandas
import shelve
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)
def conv2d(x, w):
    return tf.nn.conv2d(x, w, strides=[1, 1, 1, 1], padding="SAME")
def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                          strides=[1, 2, 2, 1], padding="SAME")




# data = shelve.open('Sex_outer.dat')
# X = data['Data']
# Y = data['Target']
# Y = Y.reshape((-1,1))
# data.close()
# Encoder = preprocessing.OneHotEncoder()
# Y = Encoder.fit_transform(Y).todense()
from sklearn import datasets
data = datasets.load_digits()
X = data.data
Y = data.target
Encoder = preprocessing.OneHotEncoder()
Y = Encoder.fit_transform(Y.reshape(-1,1)).todense()

x = tf.placeholder(tf.float32, shape=(None, 64), name='x')
y_ = tf.placeholder(tf.float32, shape=(None, 10), name='y')

x_image = tf.reshape(x, [-1, 8, 8, 1])
W_conv1 = weight_variable([2, 2, 1, 32])
b_conv1 = bias_variable(shape=[32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable([2, 2, 32, 64])
b_conv2 = bias_variable(shape=[64])
h_conv2 = tf.nn.sigmoid(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_fc1 = weight_variable([2 * 2 * 64, 64])
b_fc1 = bias_variable([64])
h_pool2_flat = tf.reshape(h_pool2, [-1, 2 * 2 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)
W_fc2 = weight_variable([64, 10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

predict = tf.argmax(y_conv, 1)
cross_entropy = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y_conv, 1e-30, 1)))
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))

batch_size = 100
dataset_size = X.shape[0]
learning_rate = 1e-3
decay_rate = 0.99
N_iteration  = 2000
global_step = tf.Variable(0, trainable=False)
learning_rate_with_decay = tf.train.exponential_decay(learning_rate=learning_rate,
                                                      global_step=global_step,
                                                      decay_steps=100,
                                                      decay_rate=decay_rate)

file1 = open('train_log.txt', 'w+')
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate_with_decay). \
    minimize(cross_entropy, global_step=global_step)
# train_step = tf.train.AdamOptimizer(learning_rate=0.0004).\
#                                   minimize(cross_entropy)

saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)
with tf.Session() as session:
    session.run(tf.initialize_all_variables())
    for i in range(N_iteration):
        start = (i * batch_size) % dataset_size
        end = numpy.min([dataset_size, start + batch_size])
        #        print (start,end)
        if i % 10 == 0:
            train_accuracy = session.run(accuracy, feed_dict={x: X[start:end, :],
                                                              y_: Y[start:end, :],
                                                              keep_prob: 0.95})
            train_loss = session.run(cross_entropy, feed_dict={x: X[start:end, :],
                                                               y_: Y[start:end, :],
                                                               keep_prob: 0.95})
            learning_rate_real = session.run(learning_rate_with_decay)

            ss = "step:%5d corss-entropy:%-10f training accuracy:%-10f learing_rate:%-10s" \
                 % (i, train_loss, train_accuracy, learning_rate_real)
            file1.write(ss + '\n')
            print(ss)
        train_step.run(feed_dict={x: X[start:end, :], y_: Y[start:end, :], keep_prob: 0.95})
    # Test_X = pandas.read_csv('test.csv', header=0)
    # Test_Y = session.run(predict, feed_dict={x: Test_X.values, keep_prob: 0.95})
    # sub = pandas.DataFrame(None, columns=['ImageId', 'Label'])
    # sub['ImageId'] = Test_X.index + 1
    # sub['Label'] = Test_Y
    # sub.to_csv('submission0621.csv', index=False, header=True)
    saver.save(session, "SexRecognize.ckpt")
file1.close()