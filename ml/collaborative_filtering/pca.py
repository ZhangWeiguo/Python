# -*-encoding:utf8-*-

import numpy

class PCA():
    def __init__(self,n_components = 0,min_score = 0):
        if n_components < 1:
            self.n_compoents = 0
        else:
            self.n_compoents = n_components
        if min_score <= 0 or min_score > 1:
            self.min_socre = 1
        else:
            self.min_socre = min_score
    def train(self,data):
        n_samples, n_dimsion = data.shape
        data_mean = data - numpy.repeat(numpy.mean(data, 0).reshape(1, -1), n_samples, axis=0)
        data_cov = numpy.cov(data_mean.T)
        eigvals, eigvects = numpy.linalg.eig(numpy.mat(data_cov))
        self.eigvals = eigvals
        self.eigects = eigvects
        self.data_mean = numpy.mean(data, 0)
        Y = data_mean * eigvects
        if self.n_compoents == 0:
            for i in range(n_dimsion):
                if numpy.sum(eigvals[0:i+1]) > self.min_socre:
                    self.score = numpy.sum(eigvals[0:i+1])
                    self.n_compoents = i+1
                    break
            data_pca = Y[:,0:i+1]
        else:
            if self.n_compoents <= n_dimsion:
                data_pca = Y[:, 0:self.n_compoents]
            else:
                data_pca = Y
        return data_pca
    def transform(self,data):
        n_samples, n_dimsion = data.shape
        data_mean = data - numpy.repeat(self.data_mean.reshape(1, -1), n_samples, axis=0)
        data_pca = data_mean * self.eigvects
        data_pca = data_pca[:,0:self.n_compoents]
        return data_pca

if __name__ == "__main__":
    from sklearn import datasets
    from matplotlib import pyplot
    data = datasets.load_digits()
    X = data.data
    Y = data.target
    pca = PCA(n_components=2)
    X1 = pca.train(X)
    Y = Y.reshape(-1, )
    pyplot.scatter(list(X1[:,0]),list(X1[:,1]),c = Y)
    pyplot.show()







