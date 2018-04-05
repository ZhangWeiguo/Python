#-*-coding:utf-8-*-
'''
created by zwg in 2016-10-5
'''
#一般回归
import numpy
from sklearn import linear_model
from matplotlib import pyplot as pl
#单自变量单因变量线性回归
class two_fit:
    def loaddata(self,x,y):
        '''
        导入数据并进行拟合
        '''
        n=len(x)
        x=numpy.array(x)
        y=numpy.array(y)
        x=x.reshape((n,1))
        y=y.reshape((n,1))
        self.x=x;self.y=y;
        self.reg=linear_model.LinearRegression()
        self.reg.fit(x,y)
        self.a=self.reg.coef_
        self.b=self.reg.intercept_
    def predict(self,x0):
        '''
        预测数据
        '''
        y0=self.reg.predict(x0)
        return y0
    def getcoef(self):
        '''
        获取拟合系数
        '''
        return self.a[0,0],self.b[0]
    def show(self):
        figure1=pl.figure()
        pl.plot(self.x,self.y,'ro',label='origin data')
        pl.plot(self.x,self.predict(self.x),label='fitting data')
        pl.legend()
        pl.show()
#多自变量单因变量线性回归
class n_fit:
    def loaddata(self,x,y):
        n=len(y)
        x=numpy.array(x)
        y=numpy.array(y)
        y.reshape((n,1))
        self.x=x;self.y=y;
        self.reg=linear_model.LinearRegression()
        self.reg.fit(x,y)
        self.a=self.reg.coef_
        self.b=self.reg.intercept_
    def predict(self,x0):
        y0=self.reg.predict(x0)
        return y0
    def getcoef(self):
        return self.a,self.b
    def show(self):
        figure1=pl.figure()
        pl.plot(range(len(self.y)),self.y,'ro',label='origin data',figure=figure1)
        pl.plot(range(len(self.y)),self.predict(self.x),label='fitting data',figure=figure1)
        pl.legend()
        pl.show()
#多自变量多独立因变量的线性回归
class nn_fit:
    def loaddata(self,x,y):
        x=numpy.array(x)
        y=numpy.array(y)
        reg=linear_model.LinearRegression()
        reg.fit(x,y)
        a=reg.coef_
        b=reg.intercept_
        self.x=x
        self.y=y
        self.reg=reg
        self.a=a
        self.b=b
    def predict(self,x0):
        y0=self.reg.predict(x0)
        return y0
    def predict_one(self,x0,k):
        '''
        预测第k个函数的秩
        '''
        x0=numpy.array(x0)
        x0.reshape((len(x0),1))
        y0=numpy.dot(self.a[k-1:k,:],x0.T)+self.b[k]
        return y0
        
#测试有效性
def test_two_fit():        
    #x=numpy.arange(1,10,0.5)
    #y=x*0.1+3
    x=[ 1 ,2  ,3 ,4 ,5 ,6]
    y=[ 2.5 ,3.51 ,4.45 ,5.52 ,6.47 ,7.51]
    fit=two_fit()
    fit.loaddata(x,y)
    x0=14
    y0=fit.predict(x0)
    a,b=fit.getcoef()
    print 'f(x0):',y0
    print 'function:ax+b (','a=',a,'b=',b,')'
    fit.show()
def test_n_fit():
    x1=numpy.arange(2,10,0.1)
    x2=numpy.linspace(2,100,len(x1))
    y=x1*0.3+x2*0.4+0.5
    x=numpy.c_[x1,x2]
    y1=y+numpy.random.random(y.shape)
    nfit=n_fit()
    nfit.loaddata(x,y1)
    x0=numpy.array([[1,1],[2,2]])
    y0=nfit.predict(x0)
    a,b=nfit.getcoef()
    print 'x0:',x0
    print 'f(x0):',y0
    print 'function:y=ax+b (','a=',a,'b=',b,')'
    nfit.show()
if __name__=='__main__':
    #test_n_fit()
    test_two_fit()