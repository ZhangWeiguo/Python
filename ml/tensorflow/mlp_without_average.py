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
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


data = pandas.read_csv('../digit/train.csv',header=0)
XX = data.ix[:,1:].values
YY = data.ix[:,0].values.reshape((-1,1))
onehot = preprocessing.OneHotEncoder()
YY = onehot.fit_transform(YY).todense()
X,X_V,Y,Y_V = train_test_split(XX, YY)

input_dimision = 784
output_dimision = 10
layer_dimision = 800

train_size = X.shape[0]
batch_size = 1500
learning_rate = 0.001
learning_rate_decay = 0.5
decay_steps = 2000
regular_rate = 0.00101
train_steps = 20000
moving_average_decay = 0.99

def inference(input_tensor, weight1, bias1, weight2, bias2):
    layer1 = tf.nn.relu(tf.matmul(input_tensor, weight1)+bias1)
    output = tf.matmul(layer1, weight2) + bias2
    return output

def train(X, Y):
    x = tf.placeholder(tf.float32, shape = [None,input_dimision], name = 'x-input')
    y_ = tf.placeholder(tf.float32, shape = [None,output_dimision], name = 'y-output')
    weight1 = tf.Variable(tf.random_normal(shape = [input_dimision, layer_dimision]))
    # bias1 = tf.Variable(tf.constant(0.1, shape = [layer_dimision]))
    bias1 = tf.Variable(tf.random_normal(shape=[layer_dimision]))
    weight2 = tf.Variable(tf.random_normal(shape = [layer_dimision, output_dimision]))
    # bias2 = tf.Variable(tf.constant(0.1, shape = [output_dimision]))
    bias2 = tf.Variable(tf.random_normal(shape=[output_dimision]))
    y = inference(x, weight1, bias1, weight2, bias2)
 

    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=y,labels=y_)
    # cross_entropy = -y_*tf.log(tf.clip_by_value(tf.nn.softmax(y),1e-10,1.0))
    
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    
    regularizer = tf.contrib.layers.l2_regularizer(regular_rate)
    regular_loss = regularizer(weight1) + regularizer(weight2)
    loss = cross_entropy_mean + regular_loss
    
    
    
    predict = tf.argmax(tf.nn.softmax(y),1)
    # predict = tf.argmax(y,1)
    
    accuracy_all = tf.equal(predict,tf.argmax(y_,1))
    accuracy = tf.reduce_mean(tf.cast(accuracy_all,tf.float64))
    # accuracy2 = tf.cast(accuracy_all,tf.float64)
    global_step = tf.Variable(0,trainable = False )
    learning_rate_with_decay = tf.train.exponential_decay(learning_rate = learning_rate,
                                      global_step = global_step,
                                      decay_steps = decay_steps,
                                      decay_rate = learning_rate_decay)
    
    
    train_step = tf.train.GradientDescentOptimizer(learning_rate_with_decay).minimize(loss,
                                                  global_step = global_step)

    
    
    with tf.Session() as session:
        session.run(tf.initialize_all_variables())
        for i in range(train_steps):
            start = (i*batch_size) % X.shape[0]
            end = numpy.min([X.shape[0], start+batch_size])
            train_step.run(feed_dict = {x: X[start:end,:], 
                                        y_: Y[start:end,:]})
#            print (start, end)
            if i%100 == 0:
                score = session.run(cross_entropy_mean, feed_dict = {x: X_V, y_: Y_V})
                acc = session.run(accuracy, feed_dict = {x:X_V, y_:Y_V})
                print ('%-7s: %-10s  %-10f'%(str(i),str(round(score,8)),acc))
                print (session.run(learning_rate_with_decay))
                # s = session.run(accuracy2,feed_dict = {x:X_V, y_:Y_V})
                # print (numpy.sum(s)/10500)
        return session.run(predict, feed_dict = {x:X_V, y_:Y_V})
                
            
            
y2= train(X,Y)
y3 = numpy.argmax(Y_V,axis=1)
s = y2.reshape((-1,1))==y3
print (numpy.sum(s))
#import gc
#gc.collect()
#y_test = numpy.argmax(Y_V,axis=1)

#a1=tf.constant([1,2,3,4,5])
#a2=tf.constant([1,2,2,4,3])
#b1=tf.cast(tf.equal(a1,a2),tf.float16)
#b=tf.reduce_mean(b1)
#
#with tf.Session() as session:
#    print (session.run(b))
#          
            
#learning_rate = 0.9
#learning_rate_decay = 0.99
#global_step = tf.Variable(0,trainable=False)
#N = 1000
#batch_size = 100 
#learning = tf.train.exponential_decay(learning_rate = learning_rate,
#                                      global_step = global_step,
#                                      decay_steps = 100,
#                                      decay_rate = learning_rate_decay)
#
#with tf.Session() as session:
#    session.run(tf.initialize_all_variables())
#    for i in range(10000):
#        global_step = global_step + 1
#        if i%1000 == 0:
#            print (session.run(global_step))
#            print (0.9*0.99**(float(i)/100))
#            print (session.run(learning))

  
    
    
    
    
    
                    