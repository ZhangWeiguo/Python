# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-04-10
'''

from theano import tensor
import theano
import numpy

x1=tensor.fscalar('x1')
x2=tensor.fvector('x2')
x3=tensor.fmatrix('x3')
x4=tensor.ftensor3('x4')
x5=tensor.ftensor4('x5')

fun1=theano.function(inputs=[x1,x2],outputs=x1+x2)
fun2=theano.function(inputs=[x3],outputs=tensor.dot(x3,x3))
fun3=theano.function(inputs=[x2,theano.In(x1,value=3)],outputs=x1*x2)


print fun1(1.0,[1,2,3])
print fun2([[1.0,2.0],[2.0,1.0]])
print fun3([4.0,4.0,2.0])






