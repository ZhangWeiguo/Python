#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 17 03:08:48 2017
@author: zwg
"""

import tensorflow as tf
import numpy, pandas, random
import shelve
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from self_data_pre import Sex_file

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
def max_pool_4x4(x):
    return tf.nn.max_pool(x, ksize=[1, 4, 4, 1],
                          strides=[1, 4, 4, 1], padding="SAME")

def get_image():
    data = shelve.open(Sex_file)
    X = data['Data']
    Y = data['Target']
    Y = Y.reshape((-1,1))
    data.close()
    return X,Y


X,Y = get_image()
print (X.shape)
x = tf.placeholder(tf.float32, shape=(None, 16384), name='x')
y_ = tf.placeholder(tf.float32, shape=(None, 1), name='y')

x_image = tf.reshape(x, [-1, 128, 128, 1])

W_conv1 = weight_variable([16, 16, 1, 16])
b_conv1 = bias_variable(shape=[16])
h_conv1 = tf.nn.sigmoid(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_4x4(h_conv1)

W_conv2 = weight_variable([32, 32, 16, 64])
b_conv2 = bias_variable(shape=[64])
h_conv2 = tf.nn.sigmoid(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_4x4(h_conv2)

W_conv3 = weight_variable([4, 4, 64, 128])
b_conv3 = bias_variable(shape=[128])
h_conv3 = tf.nn.sigmoid(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x2(h_conv3)


W_fc1 = weight_variable([4 * 4 * 128, 512])
b_fc1 = bias_variable([512])
h_pool2_flat = tf.reshape(h_pool3, [-1, 4 * 4 * 128])
h_fc1 = tf.nn.sigmoid(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)
keep_prob = tf.placeholder(tf.float32,name = 'keep_prob')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# W_fc3 = weight_variable([512, 512])
# b_fc3 = bias_variable([512])
# y_conv_1 = tf.sigmoid(tf.matmul(h_fc1_drop, W_fc3) + b_fc3)

W_fc2 = weight_variable([512, 1])
b_fc2 = bias_variable([1])
y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
predict = 1.0/(1.0+tf.exp(-y_conv))
cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels =y_,logits=y_conv))
# cross_entropy = -tf.reduce_mean(y_ * tf.log(predict) + (1-y_)*tf.log(1-predict))
correct_prediction = tf.equal(tf.round(predict), y_)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))

batch_size = 128
dataset_size = X.shape[0]
learning_rate = 0.0001
decay_rate = 0.85
N_iteration =  1500
global_step = tf.Variable(0, trainable=False)
learning_rate_with_decay = tf.train.exponential_decay(learning_rate=learning_rate,
                                                      global_step=global_step,
                                                      decay_steps=500,
                                                      decay_rate=decay_rate)

file1 = open('train_log.txt', 'w+')
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate_with_decay). \
    minimize(cross_entropy, global_step=global_step)
# train_step = tf.train.GradientDescentOptimizer(learning_rate=learning_rate_with_decay). \
#     minimize(cross_entropy, global_step=global_step)
# train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
saver = tf.train.Saver()
tf.add_to_collection('predict', predict)
with tf.Session() as session:
    # session.run(tf.initialize_all_variables())
    session.run(tf.global_variables_initializer())
    for i in range(N_iteration):
        start = (i * batch_size) % dataset_size
        end = numpy.min([dataset_size, start + batch_size])
        L = random.sample(range(dataset_size), batch_size)
        #        print (start,end)
        if i % 10 == 0:
            train_accuracy = session.run(accuracy, feed_dict={x: X[100:200, :],
                                                              y_: Y[100:200, :],
                                                              keep_prob: 0.95})
            train_loss = session.run(cross_entropy, feed_dict={x: X[100:200, :],
                                                               y_: Y[100:200, :],
                                                               keep_prob: 0.95})
            learning_rate_real = session.run(learning_rate_with_decay)

            ss = "step:%5d corss-entropy:%-10f training accuracy:%-10f learing_rate:%-10s" \
                 % (i, train_loss, train_accuracy, learning_rate_real)
            file1.write(ss + '\n')
            print(ss)
        # train_step.run(feed_dict={x: X[start:end, :], y_: Y[start:end, :], keep_prob: 0.95})
        train_step.run(feed_dict={x: X[L, :], y_: Y[L, :], keep_prob: 0.95})
    saver.save(session, "./SelfRecognize.ckpt")
file1.close()