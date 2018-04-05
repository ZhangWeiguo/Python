# -*- coding: utf-8 -*-
"""
Created on Sat Oct 01 15:01:54 2016
@author: zhangweiguo
"""
import sympy,numpy
import math
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D as ax3
#最速下降法，二维实验
def SD(x0,N,E,f,f_d):
	X=x0;Y=[];Y_d=[];
	n = 1
	ee = f_d(x0)
	e=(ee[0]**2+ee[1]**2)**0.5
	Y.append(f(x0)[0,0]);Y_d.append(e)
	a=sympy.Symbol('a',real=True)
	print '第%d次迭代：e=%d' % (n, e)
	while n<N and e>E:
		n=n+1
		yy=f(x0-a*f_d(x0))
		yy_d=sympy.diff(yy[0,0],a,1)
		a0=sympy.solve(yy_d)
		x0=x0-a0*f_d(x0)
		X=numpy.c_[X,x0]
		Y.append(f(x0)[0,0])
		ee = f_d(x0)
		e = math.pow(math.pow(ee[0,0],2)+math.pow(ee[1,0],2),0.5)
		Y_d.append(e)
		print '第%d次迭代：e=%s'%(n,e)
	return X,Y,Y_d
if __name__=='__main__':
	G=numpy.array([[21.0,4.0],[4.0,15.0]])
	#G=numpy.array([[21.0,4.0],[4.0,1.0]])
	b=numpy.array([[2.0],[3.0]])
	c=10.0
	f = lambda x: 0.5 * (numpy.dot(numpy.dot(x.T, G), x)) + numpy.dot(b.T, x) + c
	f_d = lambda x: numpy.dot(G, x) + b
	x0=numpy.array([[-30.0],[100.0]])
	N=40
	E=10**(-6)
	X, Y, Y_d=SD(x0,N,E,f,f_d)
	X=numpy.array(X)
	Y=numpy.array(Y)
	Y_d=numpy.array(Y_d)
	figure1=pl.figure('trend')
	n=len(Y)
	x=numpy.arange(1,n+1)
	pl.subplot(2,1,1)
	pl.plot(x,Y,'r*',markersize=10)
	pl.xlabel('n')
	pl.ylabel('f(x)')
	pl.subplot(2,1,2)
	pl.semilogy(x,Y_d,'g*--',markersize=10)
	pl.xlabel('n')
	pl.ylabel("|f'(x)|")
	figure2=pl.figure('behave')
	x1=numpy.arange(-110,110,1)
	y1=x1
	[xx,yy]=numpy.meshgrid(x1,y1)
	zz=numpy.zeros(xx.shape)
	n=xx.shape[0]
	for i in xrange(n):
		for j in xrange(n):
			xxx=numpy.array([xx[i,j],yy[i,j]])
			zz[i,j]=f(xxx.T)
	pl.contour(xx,yy,zz,15)
	pl.plot(X[0,:],X[1,:],'ro--')
	pl.show()