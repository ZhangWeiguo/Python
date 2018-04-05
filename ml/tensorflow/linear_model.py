import tensorflow as tf
import os,numpy
from sklearn import datasets
import random
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'



data = datasets.make_friedman2(n_samples = 10000, noise = 0)
x,y = data
y = numpy.sum(x,axis = 1)
y = y.reshape((-1,1))
N, M_x = x.shape
N, M_y = y.shape
print (x.shape, y.shape)
learing_rate = 0.0001
train_round = 15000
batch_size = 200
hidden_layer_size = 300

# a = tf.constant(value = [[1,2],[3,4]])
# b = tf.constant(value = [[3,2],[1,2]])
# c1 = tf.matmul(a, b)


X = tf.placeholder(shape = (None, M_x), dtype = tf.float32, name = 'x')
Y = tf.placeholder(shape = (None, M_y), dtype = tf.float32, name = 'y')

w0 = tf.Variable(initial_value = tf.truncated_normal(shape = (M_x, hidden_layer_size)), dtype = tf.float32)
b0 = tf.Variable(initial_value = tf.random_normal(shape = (hidden_layer_size,)), dtype = tf.float32)

w1 = tf.Variable(initial_value = tf.truncated_normal(shape = (hidden_layer_size, M_y)), dtype = tf.float32)
b1 = tf.Variable(initial_value = tf.truncated_normal(shape = (M_y,)), dtype = tf.float32)

Y_hidden = tf.matmul(X, w0) + b0
Y_pre = tf.matmul(Y_hidden, w1) + b1

# w0 = tf.Variable(initial_value = tf.truncated_normal(shape = (M_x, M_y)), dtype = tf.float32)
# b0 = tf.Variable(initial_value = tf.random_normal(shape = (M_y,)), dtype = tf.float32)
# Y_pre = tf.matmul(X, w0) + b0
global_step = tf.Variable(0, trainable = False)
learing_rate_with_decay = tf.train.exponential_decay(learing_rate, global_step, 2000, 0.95)

Loss = tf.reduce_mean(tf.square(Y_pre - Y))
train_step = tf.train.AdamOptimizer(learning_rate = learing_rate_with_decay,
									name = 'adam')
train = train_step.minimize(loss = Loss, global_step = global_step)


initial = tf.global_variables_initializer()

saver = tf.train.Saver()

with tf.Session() as session:
	session.run(initial)
	# print (session.run(Y_pre.shape))
	for i in range(train_round):
		start = i*batch_size % N
		end = min([N, start+batch_size])
		# print (start,end)
		train_index = range(start, end)
		x_train = x[train_index, :]
		y_train = y[train_index, :]
		# print (x_train.shape, y_train.shape)
		if i%100 == 0:
			error = session.run(Loss, feed_dict = {X: x, Y: y})
			print ('The %-3d round the error is %-7f'%(i, error))
		session.run(train, feed_dict = {X: x_train, Y: y_train})
	saver.save(session, './0706.ckpt')

