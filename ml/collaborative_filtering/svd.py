# -*-encoding:utf-8-*-


from numpy.linalg import svd
from scipy.sparse import linalg
import numpy,random

class SVD():
    def __init__(self):
        pass
    @staticmethod
    def transform_custom(data, transpose = False):
        if transpose:
            A = numpy.dot(data,data.T)
            eigvals,eigvectors = numpy.linalg.eig(A)
            A_sort = numpy.argsort(eigvals)
            L = range(len(A_sort))
            L.reverse()
            A_sort = A_sort[L]
            eigvals = numpy.sqrt(numpy.maximum(eigvals[A_sort],1e-30))
            eigvectors = eigvectors[:,A_sort]
            S = numpy.diag(eigvals)
            S_ni = numpy.linalg.pinv(S)
            V = eigvectors
            U = numpy.dot(numpy.dot(data.T,eigvectors.T),S_ni)
            E = V.T
            V = U.T
            U = E
            return U,S,V
        else:
            A = numpy.dot(data.T,data)
            eigvals,eigvectors = numpy.linalg.eig(A)
            A_sort = numpy.argsort(eigvals)
            L = range(len(A_sort))
            L.reverse()
            A_sort = A_sort[L]
            eigvals = numpy.sqrt(numpy.maximum(eigvals[A_sort],1e-30))
            eigvectors = eigvectors[:,A_sort]
            S = numpy.diag(eigvals)
            S_ni = numpy.linalg.pinv(S)
            V = eigvectors.T
            U = numpy.dot(numpy.dot(data,eigvectors),S_ni)
            return U,S,V

    @staticmethod
    def transform_dense(data):
        a,b,c = svd(data,full_matrices = False)
        b = numpy.diag(b)
        return a,b,c
    @staticmethod
    def transform_sparse(data):
        a,b,c = linalg.svds(data)
        return a,numpy.diag(b),c


class SVD_SG():
    def __init__(self,n_dimsion):
        self.n_dimsion = n_dimsion
    def train(self, data,
              n_iteration = 1000,
              max_error = 0.0001,
              step = 0.001,
              alpha1 = 0.01,
              alpha2 = 0.01):
        M,N = data.shape
        self.user_vector = numpy.random.rand(M,self.n_dimsion)
        self.item_vector = numpy.random.rand(N,self.n_dimsion)
        M_s = range(M)
        N_s = range(N)
        random.shuffle(M_s)
        random.shuffle(N_s)
        for k in range(n_iteration):
            for i in M_s:
                for j in N_s:
                    x = numpy.dot(self.user_vector[i:i+1,:],(self.item_vector[j:j+1,:]).T)[0,0]
                    du = -2*(data[i,j] - x)*self.item_vector[j:j+1,:] + 2*alpha1*self.user_vector[i:i+1,:]
                    di = -2*(data[i,j] - x)*self.user_vector[i:i+1,:] + 2*alpha2*self.item_vector[i:i+1,:]
                    self.user_vector[i:i + 1, :] -= step * du
                    self.item_vector[j:j + 1, :] -= step * di
                    e = self.error(data)
                    if e < max_error:
                        return
            print self.error(data)
    def error(self,data):
        E = numpy.mean((numpy.dot(self.user_vector,self.item_vector.T) - data)**2)
        return E

if __name__ == "__main__":
    A = numpy.random.rand(100,120)
    print SVD.transform_custom(A,transpose=False)[1]
    print SVD.transform_dense(A)[1]
    S = SVD_SG(20)
    S.train(A)
    print S.user_vector,S.item_vector
