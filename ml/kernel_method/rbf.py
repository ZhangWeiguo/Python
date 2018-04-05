# -*- coding: utf-8 -*-
"""
Created on Fri Oct 07 09:29:46 2016

@author: zhangweiguo
"""
'''
这里用RBF解决一维和二维的数据拟合问题
所选用基函数有MQ，高斯，多项式
'''

import numpy
from matplotlib import pyplot as pl
from mpl_toolkits.mplot3d import Axes3D as ax3
class RBF_1D:
    def createdata(self,X,Y,basicname='MQ',method='pinv',*args):
        #X,Y为拟合数据，basicname为基函数选择：MQ，Gaussian，Poly
        #method为解方程的方法：inv，pinv
        #args为基函数的参数
        X=numpy.array(X)
        Y=numpy.array(Y)
        n=len(X)
        X=X.reshape((n,1))
        Y=Y.reshape((n,1))
        #basic1为MQ基函数，参数c，beta
        #basic2为高斯基函数，参数a
        #basic3为多项式基函数，参数N
        c,beta=args
        a=args[0]
        N=args[0]
        basic1=lambda x:(x-c**2)**beta
        basic2=lambda x:numpy.exp(-numpy.power(x/a,2))
        basic3=lambda x:x**N
        basicfunction={'MQ':basic1,'Gaussian':basic2,'Poly':basic3}
        basic=basicfunction[basicname]

        A=numpy.zeros((n,n))
        XX=numpy.zeros((n,n))
        F=numpy.zeros((n,1))
        a=numpy.zeros((n,1))
        for i in xrange(n):
            for j in xrange(n):
                XX[i,j]=(X[i,0]-X[j,0])**2
                A[i,j]=basic(XX[i,j])
        F=Y.copy()
        if method=='inv':
            a=numpy.dot(numpy.linalg.inv(A),F)
        else:
            a=numpy.dot(numpy.linalg.pinv(A),F)
        self.x=X
        self.y=Y
        self.a=a
        self.basic=basic
    def predict(self,x0):
        x0=numpy.array(x0)
        x0.reshape((len(x0),1))
        n1=len(self.x)
        n2=len(x0)
        A=numpy.zeros((n2,n1))
        for i in xrange(n2):
            for j in xrange(n1):
                ans=(x0[i]-self.x[j])
                ans=ans**2
                A[i,j]=self.basic(ans)
        F=numpy.dot(A,self.a)
        return F
    def show(self):
        #展示逼近情况并返回误差向量
        figure1=pl.figure()
        pl.plot(self.x,self.y,'y<',label='origin data')
        y=self.predict(self.x)
        error=numpy.abs(y-self.y)
        pl.plot(self.x,y,label='fitting data')
        pl.legend()
        figure1.show()
        return error

class RBF_2D:
    def createdata(self,x1,x2,y,basicname,method,*args):
        #x1,x2的长度必须相同
        c,beta=args
        a=args[0]
        N=args[0]
        basic1=lambda x:(x-c**2)**beta
        basic2=lambda x:numpy.exp(-numpy.power(x/a,2))
        basic3=lambda x:x**N
        basicfunction={'MQ':basic1,'Gaussian':basic2,'Poly':basic3}
        basic=basicfunction[basicname]
        x1=numpy.array(x1)
        x2=numpy.array(x2)
        y=numpy.array(y)
        n=len(x1)
        x1=x1.reshape((n,1))
        x2=x2.reshape((n,1))
        y=y.reshape((n,1))

        A=numpy.zeros((n,n))
        XX=numpy.zeros((n,n))
        F=numpy.zeros((n,1))
        a=numpy.zeros((n,1))
        for i in xrange(n):
            for j in xrange(n):
                XX[i,j]=((x1[i,0]-x1[j,0])**2+(x2[i,0]-
                x2[j,0])**2)**0.5
                A[i,j]=basic(XX[i,j])
        F=y.copy()
        if method=='inv':
            a=numpy.dot(numpy.linalg.inv(A),F)
        else:
            a=numpy.dot(numpy.linalg.pinv(A),F)
        self.x1=x1
        self.x2=x2
        self.y=y
        self.a=a
        self.basic=basic
    def predict(self,xx1,xx2):
        n1=len(xx1)
        n2=len(self.x1)
        xx1=numpy.array(xx1).reshape((n1,1))
        xx2=numpy.array(xx2).reshape((n1,1))
        A=numpy.zeros((n1,n2))
        basic=self.basic
        x1=self.x1
        x2=self.x2
        a=self.a
        for i in xrange(n1):
            for j in xrange(n2):
                A[i,j]=basic(((xx1[i,0]-x1[j,0])**2+
                (xx2[i,0]-x2[j,0])**2)**0.5)
        F=numpy.dot(A,a)
        return F
    def show(self):
        #展示逼近情况并返回误差向量
        figure1=pl.figure()
        ax=ax3(figure1)
        ax.scatter3D(self.x1,self.x2,self.y)
        y=self.predict(self.x1,self.x2)
        error=numpy.abs(y-self.y)
        ax.plot3D(self.x1,self.x2,self.y[:,0],'r',figure=figure1)
        pl.show()
        return error
if __name__=='__main__':
    '''
    x=numpy.arange(1,10,0.1)
    y=numpy.sin(x)
    R=RBF_1D()
    R.createdata(x,y,'Poly','pinv',0.5,3)
    error=R.show()
    x0=[3.14]
    y0=R.predict(x0)
    print y0
    print '平均误差:',numpy.mean(error)
    '''
    x1=numpy.arange(2,10,0.1)
    x2=numpy.linspace(3,20,len(x1))
    x1=numpy.array(x1)
    x2=numpy.array(x2)
    x1=x1.reshape((len(x1),1))
    x2=x2.reshape((len(x2),1))
    f=lambda x1,x2:numpy.sin(x1)+numpy.cos(2*x2)
    y=numpy.sin(x1)+numpy.cos(2*x2)
    R=RBF_2D()
    R.createdata(x1,x2,y,'MQ','pinv',0.5,3)
    xx1=numpy.random.rand(3,1)
    xx2=numpy.random.rand(3,1)
    yy=f(xx1,xx2)
    F=R.predict(x1,x2)
    print 'error:',numpy.mean(F-y)
    R.show()