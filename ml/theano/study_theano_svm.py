# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-04-10
'''


import theano
from theano import tensor
import numpy
from matplotlib import pyplot
from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.metrics import pairwise_distances,r2_score
# data=datasets.load_iris()
# X=data.data
# Y=data.target
# X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=33)


data=datasets.make_friedman1(1000,n_features=5,noise=0.5,random_state=33)
X=data[0]
Y=data[1].reshape((-1,1))
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.3,random_state=33)



class theano_svr():
    def __init__(self,k=10,ita=0.9,max_iter=700,f_tol=1e-4):
        self.X_train_dist = pairwise_distances(X_train)
        self.x = tensor.dmatrix('x')
        self.y = tensor.dmatrix('y')
        self.x_train = tensor.dmatrix('x_train')
        self.y_train = tensor.dmatrix('y_train')
        self.x_dist = tensor.dmatrix('x_dist')
        self.k = k
        self.ita = ita
        self.max_iter = max_iter
        self.f_tol = f_tol
    def fit(self,X_train,Y_train):
        (n1, n2) = X_train.shape
        (n3, n4) = Y_train.shape
        self.X_train = X_train
        self.Y_train = Y_train
        self.A0 = numpy.random.rand(n1, n4)
        self.A = theano.shared(self.A0, name='A')
        self.fine = tensor.exp(-self.k * tensor.square(self.x_dist))
        self.y = theano.dot(self.fine, self.A)
        self.loss = self.y - self.y_train
        self.error = tensor.mean(tensor.square(self.loss))
        self.gA, = tensor.grad(self.error, [self.A])
        self.train = theano.function(inputs=[self.x_dist, self.y_train],
                                     outputs=self.error,
                                     updates=((self.A, self.A - self.ita * self.gA),))
        self.pre = theano.function(inputs=[self.x_dist],outputs=self.y)
        for i in range(self.max_iter):
            err = self.train(self.X_train_dist, self.Y_train)
            print err
            if err<self.f_tol:
                break
    def predict(self,X_test):
        X_test_dist=pairwise_distances(X_test,X_train)
        Y_test_pre=self.pre(X_test_dist)
        return Y_test_pre
    def score(self,X_test,Y_test):
        Y_test_pre=self.predict(X_test)
        score=r2_score(Y_test,Y_test_pre)
        return score

svm=theano_svr()
svm.fit(X_train,Y_train)
print svm.score(X_test,Y_test)


# X_train_dist=pairwise_distances(X_train)
# (n1,n2)=X_train.shape
# (n3,n4)=Y_train.shape
# A0=numpy.random.rand(n1,n4)
# x=tensor.dmatrix('x')
# y=tensor.dmatrix('y')
# x_train=tensor.dmatrix('x_train')
# y_train=tensor.dmatrix('y_train')
# x_dist=tensor.dmatrix('x_dist')
# A=theano.shared(A0,name='A')
# k=10
# ita=0.5
# max_iter=300
# e_tol=1e-4
#
# fine=tensor.exp(-k*tensor.square(x_dist))
# y=theano.dot(fine,A)
# loss=y-y_train
# error=tensor.mean(tensor.square(loss))
# gA,=tensor.grad(error,[A])
# # fun=theano.function(inputs=[X_train_dist],outputs=loss)
#
# train=theano.function(inputs=[x_dist,y_train],outputs=error,updates=((A,A-ita*gA),))
# for i in range(max_iter):
#     err=train(X_train_dist,Y_train)
#     print err


'''
# need improve
# (n1,n2)=X_train.shape
# (n3,n4)=Y_train.shape
# A0=numpy.random.rand(n4,n1)
# x=tensor.dmatrix('x')
# y=tensor.dmatrix('y')
# x_train=tensor.dmatrix('x_train')
# y_train=tensor.dmatrix('y_train')
# A=theano.shared(A0,name='A')
# k=10
# ita=0.7
# max_iter=200
# e_tol=1e-4

# di=tensor.sqrt(tensor.sum(tensor.square(tensor.repeat(x,n1,0)-x_train),axis=1)).reshape((-1,1))
# fine=tensor.exp(-k*tensor.square(di))
# y=theano.dot(A,fine)
# loss=y-y_train
# error=tensor.mean(tensor.square(loss))
# dA=tensor.transpose(2*tensor.dot(fine,loss),axes=(1,0))
# train=theano.function(inputs=[x,x_train,y_train],outputs=error,updates=((A,A-ita*dA),))
# for i in range(max_iter):
#     for j in range(n1):
#         err=train(X_train[i,:].reshape((1,-1)),X_train,Y_train[i,:].reshape((1,-1)))
#         print err
'''