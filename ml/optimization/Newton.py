# -*- coding:utf-8 -*-
"""
Created on Sat Oct 01 15:01:54 2016
@author: zhangweiguo
"""
import numpy
import matplotlib.pyplot as pl
from mpl_toolkits.mplot3d import Axes3D as ax3
#Newton寻优，二维实验
def NE(x0,y0,N,E):
	X1=[];X2=[];Y=[];Y_d=[]
	n = 1
	ee = g(x0,y0)
	e=(ee[0,0]**2+ee[1,0]**2)**0.5
	X1.append(x0)
	X2.append(y0)
	Y.append(f(x0,y0))
	Y_d.append(e)
	print '第%d次迭代：e=%s' % (n, e)
	while n<N and e>E:
		n=n+1
		#d=-numpy.dot(numpy.linalg.inv(G(x0,y0)),g(x0,y0))
		d=-numpy.dot(numpy.linalg.pinv(G(x0,y0)),g(x0,y0))
		x0=x0+d[0,0]
		y0=y0+d[1,0]
		ee = g(x0, y0)
		e = (ee[0,0] ** 2 + ee[1,0] ** 2) ** 0.5
		X1.append(x0)
		X2.append(y0)
		Y.append(f(x0, y0))
		Y_d.append(e)
		print '第%d次迭代：e=%s'%(n,e)
	return X1,X2,Y,Y_d
if __name__=='__main__':
	f = lambda x,y: 3*x**2+3*y**2-x**2*y                    #原函数
	g = lambda x,y: numpy.array([[6*x-2*x*y],[6*y-x**2]])   #一阶导函数向量
	G = lambda x,y: numpy.array([[6-2*y,-2*x],[-2*x,6]])    #二阶导函数矩阵
	x0=-2;y0=4
	x0=0;y0=3
	N=10;E=10**(-6)
	X1,X2,Y,Y_d=NE(x0,y0,N,E)
	X1=numpy.array(X1)
	X2=numpy.array(X2)
	Y=numpy.array(Y)
	Y_d=numpy.array(Y_d)
	figure1=pl.figure('trend')
	n=len(Y)
	x=numpy.arange(1,n+1)
	pl.subplot(2,1,1)
	pl.semilogy(x,Y,'r*',markersize=10)
	pl.xlabel('n')
	pl.ylabel('f(x)')
	pl.subplot(2,1,2)
	pl.semilogy(x,Y_d,'g*',markersize=10)
	pl.xlabel('n')
	pl.ylabel("|f'(x)|")
	figure2=pl.figure('behave')
	x=numpy.arange(-6,6,0.1)
	y=x
	[xx,yy]=numpy.meshgrid(x,y)
	zz=numpy.zeros(xx.shape)
	n=xx.shape[0]
	for i in xrange(n):
		for j in xrange(n):
			zz[i,j]=f(xx[i,j],yy[i,j])
	#ax=ax3(figure2)
	pl.contour(xx,yy,zz,15)
	#ax.contour(xx,yy,zz,15)
	pl.plot(X1,X2,'ro--')
	for i in range(len(X1)):
		pl.text(X1[i],X2[i],str(i))
	pl.show()
