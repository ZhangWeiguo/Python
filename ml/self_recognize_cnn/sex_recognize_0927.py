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
from sex_data_pre import Sex_file

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
Encoder = preprocessing.OneHotEncoder()
Y = Encoder.fit_transform(Y.reshape(-1,1)).todense()

x = tf.placeholder(tf.float32, shape=(None, 16384), name='x')
y_ = tf.placeholder(tf.float32, shape=(None, 2), name='y')
keep_prob = tf.placeholder(tf.float32,name = 'keep_prob')

W_fc1 = weight_variable([16384, 1024])
b_fc1 = bias_variable([1024])
h_fc1 = tf.nn.sigmoid(tf.matmul(x, W_fc1) + b_fc1)


W_fc2 = weight_variable([1024, 2])
b_fc2 = bias_variable([2])
y_conv = tf.nn.sigmoid(tf.matmul(h_fc1,W_fc2) + b_fc2)


# W_fc3 = weight_variable([512, 512])
# b_fc3 = bias_variable([512])
# y_conv_1 = tf.sigmoid(tf.matmul(h_fc1_drop, W_fc3) + b_fc3)

predict = tf.argmax(y_conv, 1)
#cross_entropy = -tf.reduce_sum(y_ * tf.log(tf.clip_by_value(y_conv, 1e-30, 1)))
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels = y_, logits=y_conv))
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))

batch_size = 64
dataset_size = X.shape[0]
learning_rate = 0.0001
decay_rate = 0.85
N_iteration =  100
global_step = tf.Variable(0, trainable=False)
learning_rate_with_decay = tf.train.exponential_decay(learning_rate=learning_rate,
                                                      global_step=global_step,
                                                      decay_steps=2000,
                                                      decay_rate=decay_rate)

file1 = open('train_log.txt', 'w+')
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate_with_decay). \
    minimize(cross_entropy, global_step=global_step)
# train_step = tf.train.GradientDescentOptimizer(learning_rate=learning_rate_with_decay). \
#     minimize(cross_entropy, global_step=global_step)
# train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
saver = tf.train.Saver(write_version=tf.train.SaverDef.V1)

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
            train_accuracy = session.run(accuracy, feed_dict={x: X[0:100, :],
                                                              y_: Y[0:100, :],
                                                              keep_prob: 0.95})
            train_loss = session.run(cross_entropy, feed_dict={x: X[0:100, :],
                                                               y_: Y[0:100, :],
                                                               keep_prob: 0.95})
            learning_rate_real = session.run(learning_rate_with_decay)

            ss = "step:%5d corss-entropy:%-10f training accuracy:%-10f learing_rate:%-10s" \
                 % (i, train_loss, train_accuracy, learning_rate_real)
            file1.write(ss + '\n')
            print(ss)
        # train_step.run(feed_dict={x: X[start:end, :], y_: Y[start:end, :], keep_prob: 0.95})
        train_step.run(feed_dict={x: X[L, :], y_: Y[L, :], keep_prob: 0.95})
    # Test_X = pandas.read_csv('test.csv', header=0)
    # Test_Y = session.run(predict, feed_dict={x: Test_X.values, keep_prob: 0.95})
    # sub = pandas.DataFrame(None, columns=['ImageId', 'Label'])
    # sub['ImageId'] = Test_X.index + 1
    # sub['Label'] = Test_Y
    # sub.to_csv('submission0621.csv', index=False, header=True)
    saver.save(session, "SexRecognize.ckpt")
file1.close()