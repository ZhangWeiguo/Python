import tensorflow as tf
import os,numpy
from matplotlib import pyplot

test_dir = "E:\\zhangweiguo\\Python\\VideoRecognize\\data\\sex\\image\\face\\"
# test_dir = "E:\\zhangweiguo\\Python\\VideoRecognize\\data\\outerdata\\man"
L = os.listdir(test_dir)
All_image_path = [os.path.join(test_dir,i) for i in L]
All_image_path = All_image_path[40:50]
Result = []

label_lines = ["woman","man"]
with tf.gfile.FastGFile("ManRecognize.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    for k,image_path in enumerate(All_image_path):
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        human_string = label_lines[1]
        score = predictions[0][1]
        Result.append(score)
        pyplot.figure(k)
        I = pyplot.imread(image_path)
        pyplot.imshow(I)
        pyplot.title("%s:%f"%(human_string,score))
pyplot.show()
print (Result)