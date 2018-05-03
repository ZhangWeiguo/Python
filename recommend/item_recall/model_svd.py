# -*-encoding:utf-8 -*-
# created by wegozng in 20180430
import tensorflow as tf  
import os,numpy,json,time
from get_train_feature import *


##################################################################

def recover(model_path,user_num,item_num):
    (model_parent_path,model_name) = os.path.split(model_path)
    users = {}
    items = {}
    with tf.Session() as session:
        saver = tf.train.import_meta_graph(model_path + ".meta")
        saver.restore(sess,tf.train.latest_checkpoint(model_parent_path))
        graph = tf.get_default_graph()
        user_vec =  graph.get_tensor_by_name("user_vec:0")
        item_vec =  graph.get_tensor_by_name("item_vec:0")
        for i in range(user_num):
            vec = list(session.run(user_vec, feed_dict = {user_ids:[i]})[0])
            vec = [float(i) for i in vec]
            users[i] = vec
        for i in range(item_num):
            vec = list(session.run(item_vec, feed_dict = {item_ids:[i]})[0])
            vec = [float(i) for i in vec]
            items[i] = vec
    return items,users


def train(
    train_files             = [],
    model_path              = "data/model",
    item_dim                = 100,
    user_dim                = 100,
    other_dim               = 0,
    goal_dim                = 1,
    batch_size              = 200,
    train_epochs            = 5,
    learning_rate           = 0.0001,
    learning_rate_decay     = 0.5,
    decay_steps             = 5000,
    input_regular_rate      = 0.00001):


    items       = {}
    users       = {}
    items_vdict = {}
    users_vdict = {}

    kv = 0
    ku = 0
    for i in train_files:
        f = open(i,'r')
        s = f.read().split("\n")
        L = range(len(s))
        for i in range(len(L)):
            user_id,item_id,goal = parse_line(s[i])
            if user_id != "" and not user_id in users_vdict:
                users_vdict[user_id] = ku
                ku += 1
            if item_id != "" and not item_id in items_vdict:
                items_vdict[item_id] = kv 
                kv += 1
        f.close()

    print("Users Num: %d"%len(users_vdict))
    print("Items Num: %d"%len(items_vdict))


    item_num = len(items_vdict)          # item数量
    user_num = len(users_vdict)          # user数量
    shuffle_files = shuffle(train_files)



    input_regular = tf.contrib.layers.l2_regularizer(input_regular_rate)
    user_ids  = tf.placeholder(tf.int32, shape =[None], name="user_ids")
    item_ids  = tf.placeholder(tf.int32, shape =[None], name="item_ids")
    other_vec = tf.placeholder(tf.float32,shape=[None,other_dim], name="other_vec")
    goal_vec  = tf.placeholder(tf.float32,shape=[None,goal_dim], name="goal_vec")
    user_vecs = tf.Variable(numpy.random.rand(user_num,user_dim), name = "user_vecs", dtype = tf.float32)
    item_vecs = tf.Variable(numpy.random.rand(item_num,item_dim), name = "item_vecs", dtype = tf.float32)
    user_vec  = tf.nn.embedding_lookup(
                                params              = user_vecs, 
                                ids                 = user_ids, 
                                partition_strategy  = 'mod', 
                                name                = "user_vec",
                                validate_indices    = True)
    item_vec = tf.nn.embedding_lookup(
                                params              = item_vecs, 
                                ids                 = item_ids, 
                                partition_strategy  = 'mod', 
                                name                = "item_vec",
                                validate_indices    = True,
                                max_norm            = True)
    regular = input_regular(user_vec) + input_regular(item_vec)
    output = tf.nn.sigmoid(tf.matmul(user_vec, tf.transpose(item_vec)), name = "output")

    error_without_regular  = tf.reduce_mean(tf.square(output-goal_vec))
    error = tf.add(error_without_regular, regular, name = "error")

    global_step = tf.Variable(0,trainable = False )
    learning_rate_with_decay = tf.train.exponential_decay(
        learning_rate = learning_rate,
        global_step = global_step,
        decay_steps = decay_steps,
        decay_rate = learning_rate_decay)

    train_step = tf.train.AdamOptimizer(learning_rate_with_decay).minimize(error,global_step = global_step)
    saver = tf.train.Saver()
    with tf.Session() as session:
        session.run(tf.global_variables_initializer())
        k = 0
        for epoch in range(train_epochs):
            print("Begin To Train %d Epoch"%epoch)
            for user_ids1,item_ids1,other_vec1,goal_vec1 in \
                    get_train_data(shuffle_files, batch_size, users_vdict, items_vdict):
                train_step.run(feed_dict = {user_ids   : user_ids1, 
                                            item_ids   : item_ids1,
                                            other_vec  : other_vec1,
                                            goal_vec   : goal_vec1})
                k +=1
                if k%100 == 0:
                    loss = session.run(error, feed_dict = {
                                                user_ids   : user_ids1, 
                                                item_ids   : item_ids1,
                                                other_vec  : other_vec1,
                                                goal_vec   : goal_vec1})
                    
                    print ("%6d iters: %3.4f"%(k,loss))
        
        for i in range(user_num):
            vec = list(session.run(user_vec, feed_dict = {user_ids:[i]})[0])
            vec = [float(i) for i in vec]
            users[i] = vec
        for i in range(item_num):
            vec = list(session.run(item_vec, feed_dict = {item_ids:[i]})[0])
            vec = [float(i) for i in vec]
            items[i] = vec
        saver.save(session, model_path)

    rm(shuffle_files)
    return items,users,items_vdict,users_vdict


    