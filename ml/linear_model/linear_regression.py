import numpy

class Linear_Regression:
    def __init__(self):
        pass
    def Train(self,Data,Target):
        N_x = len(Data[0])
        N_y = len(Target[0])
        self.Dimsion_x = N_x
        self.Dimsion_y = N_y
        self.Para = numpy.zeros((self.Dimsion_y,))
        self.Coef = numpy.zeros((self.Dimsion_x, self.Dimsion_y))

        batch_size = 100
        N_sample,N_dimsion = Data.shape
        E = 1e-4
        eta = 1e-2
        N_iteration = 2000
        e = self.Error(Data,Target)
        n = 0
        while e>E and n<N_iteration:
            begin = batch_size * n % N_sample
            end = min(N_sample, begin + batch_size)
            data = Data[begin:end,:]
            target = Target[begin:end,:]
            Para_grad = numpy.sum(numpy.dot(data,self.Coef)+self.Para-target, axis=0)*2/batch_size
            temp = ((numpy.dot(data,self.Coef)+self.Para-target)*2/batch_size)
            Coef_grad = numpy.dot(temp.T,data).T
            self.Coef -= Coef_grad * eta
            self.Para -= Para_grad * eta
            e = self.Error(data,target)
            n += 1
            print ("%d iteration the error is %3.8f"%(n,e))
    def Predict(self,Data):
        Target = numpy.dot(Data, self.Coef) + self.Para
        return Target
    def Error(self,Data,Target):
        Target_ = self.Predict(Data)
        Error = numpy.average(numpy.square(Target-Target_))
        return Error

if __name__ == '__main__':
    Data = numpy.random.rand(3000, 3)
    Target1 = numpy.sum(Data, axis=1) + 3.0
    Target1 = Target1.reshape((-1,1))
    Target2 = 2*numpy.sum(Data, axis=1) + 2.0
    Target2 = Target2.reshape((-1,1))
    Target = numpy.hstack((Target1,Target2))
    L = Linear_Regression()
    L.Train(Data, Target)
    Target_ = L.Predict(Data)
    Score = L.Error(Data, Target)
    print L.Para
    print L.Coef