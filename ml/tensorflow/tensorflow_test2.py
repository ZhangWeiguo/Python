#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 20:55:02 2017

@author: zwg
"""
import tensorflow as tf

a=tf.constant(1,name='a')
b=tf.Variable(0,name='b')

new_value=tf.add(a,b)
update=tf.assign(b,new_value)

initial=tf.global_variables_initializer()

with tf.Session() as session:
    session.run(initial)
    print ('initial value:',session.run(b))
    for i in range(3):
        session.run(update)
        print (session.run(b))
        




# Variables needed to be initialized
a1=tf.Variable([1,2],name='a1')
a2=tf.Variable([3,4],name='a2')
a3=tf.Variable(name='a3')
a4=tf.Variable(name='a4')
a3=tf.add(a1,a2)
a4=tf.multiply(a1,a2)
initial=tf.initialize_all_variables()

with tf.Session() as session:
    session.run(initial)
    result1=session.run(a1)
    result2=session.run(a2)
    result3=session.run([a3,a4])
    print (result1,result2)
    print (result3)


# constant do not need initial
a1=tf.constant([3,4],name='a1')
a2=tf.constant([1,2],name='a2')
a3=tf.add(a1,a2)
with tf.Session() as session:
    result1=session.run(a3)
    print (result1)


# save all the data
a1=tf.constant(9.0,name='a1')
a2=tf.constant([3.0,4.0],name='a2')
a3=tf.Variable(0,name='a3')
saver=tf.train.Saver()
initial=tf.initialize_all_variables()
with tf.Session() as session:
    session.run(initial)
    saver_path=saver.save(session,'./data1')

# restore all the data
saver=tf.train.Saver()
with tf.Session() as session:
    saver.restore(session,'./data1')
    print (session.run(a3))
    
    
    
# save part data and change the name of data (Variable)
a1=tf.constant(9.0,name='a1')
a2=tf.constant([3.0,4.0],name='a2')
a3=tf.Variable(0,name='a3')
b1=tf.constant(value=0,name='b1')
saver=tf.train.Saver({"aa3":a3})
initial=tf.initialize_all_variables()
with tf.Session() as session:
    session.run(initial)
    saver_path=saver.save(session,'./data1')
    
    
aa3=tf.Variable(10,name='aa3')
saver=tf.train.Saver()
initial=tf.initialize_all_variables()
with tf.Session() as session:
    #session.run(initial)   # It can not be run otherwise it will recover the data1
    saver.restore(session,'./data1')
    print (session.run(aa3))
    





