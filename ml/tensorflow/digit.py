# -*- encoding:utf-8 -*-
import tensorflow as tf
import os,numpy
from sklearn import datasets
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import random
from matplotlib import pyplot


# 这里是生成训练的数据和测试的数据
# 因为要进行训练，多分类任务一般会将标签转换成OneHot的编码形式
data = datasets.load_digits()
X,Y = data.data,data.target
onehot = preprocessing.OneHotEncoder()
YY = onehot.fit_transform(Y.reshape((-1,1))).todense()
x_train,x_test,y_train,y_test = train_test_split(X, YY)



# 这里定义输入输出的维度和训练的参数,其中只有一个中间层
input_dimision          = 64
output_dimision         = 10
layer_dimision          = 32
batch_size              = 100
learning_rate           = 0.0001
regular_rate            = 0.0001
train_steps             = 50000
moving_average_decay    = 0.99


# 这里定义变量
# x是输入, y是真实的输出, y_pre是模型根据x的预测输出
# y_hidden = relu((x * weight1) + bias1)
# yn =(y_hidden * weight2) + bias2
x = tf.placeholder(tf.float32, shape = [None,input_dimision], name = 'x-input')
y = tf.placeholder(tf.float32, shape = [None,output_dimision], name = 'y-output')
weight1 = tf.Variable(tf.random_normal(shape = [input_dimision, layer_dimision]))
bias1 = tf.Variable(tf.constant(0.1, shape = [layer_dimision]))
weight2 = tf.Variable(tf.random_normal(shape = [layer_dimision, output_dimision]))
bias2 = tf.Variable(tf.constant(0.1, shape = [output_dimision]))

y_hidden = tf.nn.relu(tf.matmul(x, weight1) + bias1)
y_pre = tf.matmul(y_hidden, weight2) + bias2

# 这里定义误差
# 模型就是要极小化就是y_pre和y的误差
# 这里用的误差函数是交叉熵 F(y,y_pre) = sum(y[i]*log(1/y_pre[i]))
# 交叉熵是一般的分类模型的常用误差函数
# 这里用的是一个内置的函数 tf.nn.softmax_cross_entropy_with_logits
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_pre, labels=y))

# 这里在误差上加一个正则项
regularizer = tf.contrib.layers.l2_regularizer(regular_rate)
regular_loss = regularizer(weight1) + regularizer(weight2)
loss = cross_entropy + regular_loss


# 这里定义梯度下降算子
train_step = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)


# 这里加一个分类准确性的变量,我们观察交叉熵的误差下降不够客观，我们更关注的是分类的准确性
correct_prediction = tf.equal(tf.argmax(y_pre, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float64))


# 下面开始训练
with tf.Session() as session:
    # 初始化所有变量，这是所有模型开始必备的
    session.run(tf.initialize_all_variables())
    n_samples = x_train.shape[0]
    print('%-15s: %-10s %-10s %-10s %-10s'%("iteration","corss_error","accuracy","test_error","test_acc"))
    for i in range(train_steps):
        # 获取Batch的训练数据
        start = (i*batch_size) % n_samples
        end = numpy.min([n_samples, start+batch_size])
        x_batch = x_train[start:end,:]
        y_batch = y_train[start:end,:]
        _, error, acc = session.run((train_step,cross_entropy,accuracy), feed_dict = {x: x_batch, y: y_batch})
        test_error,test_acc = session.run((cross_entropy,accuracy), feed_dict = {x: x_test, y: y_test})
        if i%100 == 0:
            print('%5d: %-3.5f %-3.5f %-3.5f %-3.5f'%(i,error,acc, test_error,test_acc))
    
    test_error,test_acc = session.run((cross_entropy,accuracy), feed_dict = {x: x_test, y: y_test})
    print("Test Corss Entropy: %3.5f  Test Accuracy: %3.5f"%(test_error,test_acc))
    y_test_pre = session.run(y_pre, feed_dict = {x: x_test})
    for i in range(4):
        xx = x_test[i]
        yy = y_test[i]
        yy_pre = y_test_pre[i]
        s = "real:%d  predict:%d"%(numpy.argmax(yy), numpy.argmax(yy_pre))
        pyplot.imshow(xx.reshape(8,8))
        pyplot.title(s)
        pyplot.show()
        