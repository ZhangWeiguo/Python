# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-04-11
'''


import numpy, theano, theano.tensor as T, gzip, cPickle

class NN():

    def __init__(self, n_in, n_out):
        self.w = theano.shared(numpy.asarray(numpy.zeros([n_in, n_out]), theano.config.floatX))
        self.b = theano.shared(numpy.asarray(numpy.zeros(n_out), theano.config.floatX))
    def get_probalblity(self, x):
        return  T.nnet.softmax(T.dot(x, self.w) + self.b)
    def get_prediction(self, x, y):
        return T.argmax(self.get_probalblity(x), 1)
    def cost(self, x, y):
        p_y_given_x = self.get_probalblity(x)
        return  -T.mean(T.log(p_y_given_x[T.arange(y.shape[0]), y]))
    def error(self, x, y):
        prediction = self.get_prediction(x, y)
        return T.mean(T.neq(prediction, y))
    def load_data(self):
        f = gzip.open('mnist.pkl.gz')
        trainxy, validatexy, testxy = cPickle.load(f)
        def share_data(xy):
            x,y = xy
            x = theano.shared(numpy.asarray(x, theano.config.floatX))
            y = theano.shared(numpy.asarray(y, theano.config.floatX))
            return [x, T.cast(y, 'int32')]
        trainx, trainy = share_data(trainxy)
        validatex,validatey = share_data(validatexy)
        testx, testy = share_data(testxy)
        return [(trainx,trainy),(validatex,validatey),(testx,testy)]
    def train(self):
        x = T.matrix('x', theano.config.floatX)
        y = T.ivector('y')
        [(trainx,trainy),(validatex,validatey),(testx,testy)] = self.load_data()
        gw,gb = T.grad(self.cost(x,y), [self.w, self.b])
        index = T.lscalar()

        batch_size = 600
        trainModel = theano.function([index], self.cost(x,y), updates=[(self.w, self.w-0.13*gw), (self.b, self.b-0.13*gb)], givens={x:trainx[index*batch_size:(index+1)*batch_size], y:trainy[index*batch_size:(index+1)*batch_size]})
        validateModel = theano.function([index], self.error(x,y), givens={x:validatex[index*batch_size:(index+1)*batch_size], y:validatey[index*batch_size:(index+1)*batch_size]})
        testModel = theano.function([index], self.error(x,y), givens={x:testx[index*batch_size:(index+1)*batch_size], y:testy[index*batch_size:(index+1)*batch_size]})

        best_validate_error = numpy.Inf
        best_test_error = 0
        patience = 5000
        increasement = 2
        train_batchs = trainx.get_value().shape[0]/batch_size
        validate_batchs = validatex.get_value().shape[0]/batch_size
        test_batchs = testx.get_value().shape[0]/batch_size
        validate_frequency = min(patience/2, train_batchs)
        epochs = 1000
        epoch = 1
        ite = 0
        stopping = False
        while (epoch < epochs) and (not stopping):
            for i in xrange(train_batchs):
                ite += 1
                this_cost = trainModel(i)
                if ite%validate_frequency == 0:
                    this_validate_error = numpy.mean([validateModel(j) for j in xrange(validate_batchs)])
                    print ('ite:%d/%d, cost:%f, validate:%f'%(ite, epoch, this_cost, this_validate_error))
                    if this_validate_error < best_validate_error:
                        if this_validate_error < 0.995*best_validate_error:
                            patience = max(patience, ite*increasement)
                        this_test_error = numpy.mean([testModel(j) for j in xrange(test_batchs)])
                        best_validate_error = this_validate_error
                        best_test_error = this_test_error
                        print ('ite:%d/%d, cost:%f, validate:%f, test:%f'%(ite, epoch, this_cost, this_validate_error, this_test_error))
                if patience <= ite:
                    stopping = True
                    break
            epoch +=1
        print ('best validate error:%f, best test error:%f'%(best_validate_error, best_test_error))


if __name__ == '__main__':
    nn = NN(784, 10)
    nn.train()