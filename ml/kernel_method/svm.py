# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 21:36:11 2017

@author: zhangweiguo
"""
import numpy

# 输入输出均为二维数组
class Linear_Svm_Regression:
    def __init__(self, C):
        self.basic = lambda x,y:numpy.dot(x,y)
        self.C = C
    def Train(self,Data,Target):
        self.Dimsion_x = len(Data[0])
        self.Dimsion_y = len(Target[0])
        N = len(Data)
        self.kernel = Data
        self.Para = numpy.random.rand(N+1, self.Dimsion_y)
        batch_size = 100
        N_sample,N_dimsion = Data.shape
        E = 1e-4
        eta = 1e-3
        N_iteration = 1000
        e = self.Error(Data,Target)
        n = 0
        for i in range(N_iteration):
            if e.all() < E:
                break
            begin = batch_size * n % N_sample
            end = min(N_sample, begin + batch_size)
            data = Data[begin:end,:]
            target = Target[begin:end,:]

            target_ = self.Predict(data)

            temp = self.basic(self.kernel, data.T)

            temp = numpy.vstack((temp, numpy.ones((1, batch_size))))


            Para_grad = self.C * self.Para * 2 / N + 2.0 / batch_size * numpy.dot(temp, target_ - target)
            self.Para -= Para_grad * eta


            e = self.Error(data,target)
            print (i,e)


    def Predict(self,Data):
        X = self.basic(Data, self.kernel.T)
        N = len(Data)
        X = numpy.hstack((X, numpy.ones((N, 1))))
        Y = numpy.dot(X, self.Para)
        return Y
    def Error(self,Data,Target):
        E1 = numpy.mean(numpy.square(self.Para), axis=0) * self.C
        E2 = numpy.mean(numpy.square(Target - self.Predict(Data)), axis=0)
        E = E1 + E2
        return E

def test():
    Data = numpy.random.rand(3000, 3)
    Target1 = numpy.sum(Data, axis=1) + 3.0
    Target1 = Target1.reshape((-1,1))
    Target2 = 2*numpy.sum(Data, axis=1) + 2.0
    Target2 = Target2.reshape((-1,1))
    Target = numpy.hstack((Target1,Target2))
    L = Linear_Svm_Regression(0)
    L.Train(Data, Target1)
    Score = L.Error(Data, Target1)
    print L.Para
    print Score
    print Target - L.Predict(Data)


if __name__ == "__main__":
    # from sklearn import svm
    # L = svm.LinearSVR()
    # Data = numpy.random.rand(3000, 3)
    # Target1 = numpy.sum(Data, axis=1) + 3.0
    # Target1 = Target1.reshape((-1,1))
    # Target2 = 2*numpy.sum(Data, axis=1) + 2.0
    # Target2 = Target2.reshape((-1,1))
    # Target = numpy.hstack((Target1,Target2))
    # L.fit(Data, Target1)
    # print L.score(Data, Target1)
    test()