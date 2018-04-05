# -*-encoding:utf-8 -*-
import numpy
from sklearn import preprocessing

# x为二维，y为一维
class Logistic_Regression_Binary():
    def __init__(self):
        self.basic = lambda x:1/(1+numpy.exp(-x))
    def Predict(self,Data):
        y = numpy.dot(Data, self.Coef.reshape((-1, 1))) + self.Para
        Target = self.basic(y)
        return Target
    def Error(self,Data,Target):
        Target_ = self.Predict(Data = Data)
        score = 0
        for i,j in zip(Target,Target_):
            score = score + numpy.log(i*j + (1-i)*(1-j))
        return score
    def Train(self,Data,Target):
        self.Dimsion = len(Data[0])
        self.Para = 0
        self.Coef = numpy.zeros(self.Dimsion,)
        batch_size = 100
        N_sample, N_dimsion = Data.shape
        E = 0
        eta = 1e-2
        N_iteration = 1000
        e = self.Error(Data, Target)
        n = 0
        while e < E and n < N_iteration:
            begin = batch_size * n % N_sample
            end = min(N_sample, begin + batch_size)
            data = Data[begin:end, :]
            target = Target[begin:end].reshape((-1, 1))
            Para_grad = numpy.sum(self.basic(numpy.dot(data, self.Coef.reshape(-1, 1)) + self.Para) - target)
            temp = (self.basic(numpy.dot(data, self.Coef.reshape(-1, 1)) + self.Para) - target).reshape((1, -1))
            Coef_grad = numpy.dot(temp, data).reshape((-1,))
            # print Coef_grad.shape, self.Coef.shape
            self.Coef -= Coef_grad * eta
            self.Para -= Para_grad * eta
            e = self.Error(data, target)
            n += 1
            print ("%d iteration the error is %3.8f" % (n, e))


# x为二维，y为二维
class Logistic_Regression_Mult():
    def __init__(self):
        self.basic = lambda x:1/(1+numpy.exp(-x))
    def Predict(self,Data):
        y = numpy.dot(Data, self.Coef) + self.Para
        Target = self.basic(y)
        T = numpy.argmax(Target, axis=1)
        T = [self.Dict[i] for i in T]
        T = numpy.array(T).reshape((-1,1))
        return T
    def Error(self,Data,Target):
        Target_ = self.Predict(Data = Data)
        N = len(Target)
        E = numpy.sum(Target == Target_ )
        error = 1-float(E)/N
        return error
    def Train(self,Data,Target):
        self.Encoder = preprocessing.OneHotEncoder()
        Target_M = numpy.array(self.Encoder.fit_transform(Target).todense())
        self.Dimsion_x = len(Data[0])
        self.Dimsion_y = len(Target_M[0])
        self.Dict = {}
        print Target_M.shape
        for i in range(len(Target)):
            if len(self.Dict.keys()) == self.Dimsion_y:
                break
            n = numpy.argmax(Target_M[i,:])
            self.Dict[n] = Target[i]
        self.Para = numpy.zeros((self.Dimsion_y,))
        self.Coef = numpy.zeros((self.Dimsion_x, self.Dimsion_y))
        print Target_M.shape
        for i in range(self.Dimsion_y):
            L = Logistic_Regression_Binary()
            y_ = Target_M[:,i]
            print Data.shape,y_.shape
            L.Train(Data,y_)
            self.Coef[:,i] = L.Coef
            self.Para[i] = L.Para

'''
def test():
    from sklearn import datasets
    from sklearn.cross_validation import train_test_split
    data = datasets.load_iris()
    Data = data.data
    Target = data.target
    Target = Target.reshape((-1,1))
    Data_train,Data_test,Target_train,Target_test = train_test_split(Data, Target)
    L = Logistic_Regression_Mult()
    L.Train(Data_train, Target_train)
    print L.Error(Data_test, Target_test)
'''


def test():
    Data = numpy.random.rand(1000, 3)
    Target1 = numpy.sum(Data, axis=1) + 3.0
    Target1[Target1 <= 5] = 1
    Target1[Target1>5] = 0
    Target = Target1.reshape((-1,1))
    L = Logistic_Regression_Mult()
    L.Train(Data, Target)
    Target_ = L.Predict(Data)
    Score = L.Error(Data, Target)
    print L.Predict(numpy.array([[1,-1,0],[2,3,4],[4,1,-3]]))
    print L.Para
    print L.Coef

if __name__  == '__main__':
    test()

