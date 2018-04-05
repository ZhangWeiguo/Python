# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-09-24
'''
import os,numpy
from matplotlib import pyplot
import tensorflow as tf
from self_data_pre import image2array,shape
test_dir = "E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\all_jpg"

Data = []
N = 5
for k,i in enumerate(os.listdir(test_dir)):
    if k>5:
        break
    Data.append(image2array(os.path.join(test_dir, i),shape = shape))
Data = numpy.array(Data)

with tf.Session() as session:
    new_saver = tf.train.import_meta_graph('./SelfRecognize.ckpt.meta')
    new_saver.restore(session, './SelfRecognize.ckpt')
    predict = tf.get_collection('predict')[0]

    graph = tf.get_default_graph()

    x = graph.get_operation_by_name('x').outputs[0]
    keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]
    Y = session.run(predict, feed_dict={x: Data,keep_prob: 0.95})

P = (1/(1+numpy.exp(-Y)))
for i in range(5):
    data = Data[i,:].reshape((shape[0],shape[1]))
    pyplot.figure()
    pyplot.imshow(data)
    pyplot.title(str(P[i]))
pyplot.show()

