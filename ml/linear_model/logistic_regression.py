# -*-encoding:utf-8 -*-
import numpy
from sklearn import preprocessing
from sklearn import datasets


class LogsiticRegression:
    def __init__(self):
        self.basic = lambda x:1/(1+numpy.exp(-x))
        self.coef = None
    
    def train(self, feature, target):
        n_sample, feature_dim = feature.shape
        _, target_dim = target.shape
        self.coef = numpy.random.rand(target_dim, feature_dim + 1)
        batch_size = 30
        epoch = 300
        eta = 0.0005
        indexs = numpy.array(list(range(n_sample)))
        for i in range(epoch):
            numpy.random.shuffle(indexs)
            start, end = 0, 0
            while start < n_sample - 1:
                end = min(start + batch_size, n_sample - 1)
                feature_t = feature[indexs[start:end], :]
                target_t = target[indexs[start:end], :]
                start += batch_size
                e = self.predict(feature_t) - target_t
                feature_tt = numpy.hstack((feature_t, numpy.ones((feature_t.shape[0], 1))))
                coef_grad = numpy.dot(numpy.transpose(e), feature_tt)
                self.coef -= eta * coef_grad
            ee = self.error(feature, target)
            sc = self.score(feature, target)
            print("%d epoch error is %3.8f score is %3.8f" % (i, ee, sc))
    
    def error(self, feature, target):
        target_pre = self.predict(feature)
        score = -numpy.sum(numpy.log(numpy.multiply(target, target_pre) + numpy.multiply((1 - target),(1 - target_pre))))
        return score

    def score(self, feature, target):
        target_pre = self.predict(feature)
        for i in range(feature.shape[0]):
            index = numpy.argmax(target_pre[i])
            target_pre[i] = 0
            target_pre[i][index] = 1
        return 1 - numpy.mean(numpy.abs(target - target_pre))        

    def predict(self, feature):
        t = numpy.ones((feature.shape[0], 1))
        feature = numpy.hstack((feature, t))
        return self.basic(numpy.dot(feature, numpy.transpose(self.coef)))