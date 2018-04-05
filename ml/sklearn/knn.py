#-*-coding:GBK-*-
'''
created by
author:zwg in 2016-10-04
'''
'''
这里用的算法很简单
KNN近邻域算法
先求测试样本到每个模板样本之间的欧氏距离
再根据模板样本的种类，求测试样本到每个种类的平均距离
距离最小的那个叫就是它所属的种类'''
import numpy
class KNN:
    def createdata(self,train,target):
        self.train=train
        self.target=target
    def classify(self,testx):
        train=self.train
        target=self.target
        n1,n2=train.shape
        test=numpy.zeros((n1,1))
        for i in xrange(n1):
            s=0
            for j in xrange(n2):
                s=s+(testx[0,j]-train[i,j])**2
            test[i,0]=s**0.5
        T=numpy.unique(target)
        nn=len(T)
        test_T=numpy.zeros((nn,1))
        for i in xrange(nn):
            test_T[i,0]=numpy.mean(test[numpy.argwhere(target==T[i])])
        position=numpy.argmin(test_T)
        testy=T[position]
        return testy
if __name__=='__main__':
    data1=numpy.random.rand(10,2)*2+10
    target1=numpy.ones((10,1))
    data2=numpy.random.rand(10,2)*3
    target2=numpy.ones((10,1))*2
    data=numpy.r_[data1,data2]
    target=numpy.r_[target1,target2]
    testx1=numpy.random.rand(1,2)*2+10
    testx2=numpy.random.rand(1,2)*3
    K=KNN()
    K.createdata(data,target)
    testy1=K.classify(testx1)
    testy2=K.classify(testx2)
    print testy1,testy2