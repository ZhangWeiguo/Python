# -*-encoding:utf-8-*-

import numpy


class CF_EASY():
    def __init__(self):
        self.cosine = lambda x,y:numpy.dot(x,y.T)/(numpy.sqrt(numpy.sum(x**2))*numpy.sqrt(numpy.sum(x**2)))
        self.euclidean = lambda x,y:numpy.sqrt(numpy.sum((x-y)**2))
    def train(self,data):
        self.data = data
    def get_user_distance(self,i,j,kind = 'cosine'):
        if kind == 'cosine':
            return self.cosine(self.data[i:i+1,:],self.data[j:j+1,:])
        if kind == 'euclidean':
            return self.euclidean(self.data[i:i + 1,:], self.data[j:j + 1,:])
        return -1
    def get_item_distance(self, i, j, kind='cosine'):
        if kind == 'cosine':
            return self.cosine(self.data[:,i:i + 1], self.data[:,j:j + 1])
        if kind == 'euclidean':
            return self.euclidean(self.data[:,i:i + 1], self.data[:,j:j + 1])
        return -1





