import numpy,os
import tensorflow as tf

model_path = "./model"
model_name = "model_test.ckpt"

def train():
    w1 = tf.Variable(tf.random_normal(shape=[2]), name='w1')
    w2 = tf.Variable(tf.random_normal(shape=[2]), name='w2')
    w3 = tf.add(w1,w2,name="w3")
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        print(sess.run(w3))
        saver.save(sess, os.path.join(model_path,model_name))
        # saver.save(sess, os.path.join(model_path,model_name), global_step=1000)

def test_withoutdefine():
    with tf.Session() as sess:    
        saver = tf.train.import_meta_graph(os.path.join(model_path,model_name) + ".meta")
        saver.restore(sess,tf.train.latest_checkpoint(model_path))
        graph = tf.get_default_graph()
        w1 = graph.get_tensor_by_name("w1:0")
        w2 = graph.get_tensor_by_name("w2:0")
        w3 = graph.get_tensor_by_name("w3:0")
        print(sess.run('w1:0'))
        print(sess.run(w1))
        print(sess.run(w3,feed_dict={w1:[3,4],w2:[4,3.3]}))


def test_withdefine():
    w1 = tf.Variable(tf.random_normal(shape=[2]), name='w1')
    w2 = tf.Variable(tf.random_normal(shape=[2]), name='w2')
    w3 = tf.add(w1,w2,name="w3")
    saver = tf.train.Saver()
    with tf.Session() as sess:    
        saver.restore(sess, os.path.join(model_path,model_name))
        print(sess.run(w1))
        print(sess.run(w3,feed_dict={w1:[3,4],w2:[4,3.3]}))

#train()
test_withdefine()
#test_withoutdefine()