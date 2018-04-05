#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 13:29:29 2017

@author: root
"""

import tensorflow as tf
import pandas,numpy
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
data = pandas.read_csv('digit/train.csv',header=0)
XX = data.ix[:,1:].values
YY = data.ix[:,0].values.reshape((-1,1))
onehot = preprocessing.OneHotEncoder()
YY = onehot.fit_transform(YY).todense()
X,X_V,Y,Y_V = train_test_split(XX, YY)

input_dimision = 784
output_dimision = 10
layer_dimision = 600

batch_size = 1000
learning_rate = 0.0001
decay_rate = 0.99
regular_rate = 0.01
train_steps = 5000
moving_average_decay = 0.99

def inference(input_tensor, avg_class, weight1, bias1, weight2, bias2):
    if avg_class == None:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, weight1)+bias1)
        output = tf.matmul(layer1, weight2) + bias2
    else:
        layer1 = tf.nn.relu(tf.matmul(input_tensor, avg_class.average(weight1))+avg_class.average(bias1))
        output = tf.matmul(layer1, avg_class.average(weight2)) + avg_class.average(bias2)
    return output

def train(X, Y):
    x = tf.placeholder(tf.float32, shape = [None,input_dimision], name = 'x-input')
    y_ = tf.placeholder(tf.float32, shape = [None,output_dimision], name = 'y-output')
    weight1 = tf.Variable(tf.random_normal(shape = [input_dimision, layer_dimision]))
    bias1 = tf.Variable(tf.constant(0.1, shape = [layer_dimision]))
    weight2 = tf.Variable(tf.random_normal(shape = [layer_dimision, output_dimision]))
    bias2 = tf.Variable(tf.constant(0.1, shape = [output_dimision]))
    y = inference(x, None, weight1, bias1, weight2, bias2)
    global_step = tf.Variable(0, trainable = False)
    
    variable_averages = tf.train.ExponentialMovingAverage(moving_average_decay, 
                                                          global_step)
    variable_averages_op = variable_averages.apply(tf.trainable_variables())
    average_y  =inference(x, variable_averages, weight1, bias1, weight2, bias2)
    
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=y, 
                                                            labels=y_)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    predict = tf.argmax(tf.nn.softmax(y),1)
    regularizer = tf.contrib.layers.l2_regularizer(regular_rate)
    regular_loss = regularizer(weight1) + regularizer(weight2)
    loss = cross_entropy_mean + regular_loss
    
    learning_rate_decay = tf.train.exponential_decay(learning_rate, global_step, 
                                              X.shape[0]/batch_size,
                                              decay_rate)
    
    
    
    train_step = tf.train.GradientDescentOptimizer(0.0001).minimize(loss,
                                                  global_step = global_step)
    with tf.control_dependencies([train_step, variable_averages_op]):
        train_op = tf.no_op(name = 'train')
    
    correct_prediction = tf.equal( tf.argmax(average_y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))
    
    with tf.Session() as session:
        session.run(tf.initialize_all_variables())
        for i in range(train_steps):
            start = (i*batch_size) % X.shape[0]
            end = numpy.min([X.shape[0], start+batch_size])
            session.run(train_op, feed_dict = {x: X[start:end,:], 
                                               y_: Y[start:end,:]})
#            print (start, end)
            if i%100 == 0:
                score_val = session.run(accuracy, feed_dict = {x: X_V, y_: Y_V})
                score_train = session.run(accuracy, feed_dict = {x:X, y_:Y})
                print ('%-6s: %-10s, %-10s'%(str(i),str(round(score_train,8)),
                                             str(round(score_val,8))))
        y2 = session.run(predict, feed_dict = {x: X_V, y_: Y_V})
    return y2
                
            
            
y2 = train(X,Y)
y3 = numpy.argmax(Y_V, axis=1)    
            
            
    
    
    
    
    
    
                    