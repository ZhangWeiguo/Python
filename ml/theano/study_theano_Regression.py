#-*- encoding:utf-8 -*-
'''
created by zwg in 2017-04-10
'''

import numpy
import theano
from theano import tensor



N=10
features=2
samplex=numpy.random.randn(N,features).astype('float32')
sampley=numpy.sum(samplex,axis=1).reshape((-1,1))*2+3

w0=numpy.random.randn(features,1)
b0=0.0
max_iter=100
max_err=1e-5


x,y=tensor.fmatrices('x','y')
w=theano.shared(w0,name='w')
b=theano.shared(b0,name='b')
predict=tensor.dot(x,w)+b
error=tensor.mean(tensor.square(predict-y))
gw,gb=tensor.grad(error,[w,b])
train=theano.function(inputs=[x,y],outputs=[predict,error],updates=((w,w-0.5*gw),(b,b-0.5*gb)))
for i in range(max_iter):
    pred,err =train(samplex,sampley)
    if err<max_err:
        break
    print '%s iterations: %s'%(str(i+1),str(round(err,3)))
print w.get_value(),b.get_value()