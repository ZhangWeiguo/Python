# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-03-30
'''
import numpy as numpy
import shelve,copy,time
from sklearn import metrics,decomposition,manifold
from sklearn import preprocessing,datasets
from matplotlib import pyplot

# tsne-固定步长+动量梯度的梯度下降 t-sne

def cal_loss(P,Q):
    C=numpy.sum(P * numpy.log(P / Q))
    return C

def cal_entropy(D,beta):
    P=numpy.exp(-D*beta)
    sumP=sum(P)
    sumP=numpy.maxmium(sumP,1e-100)
    H=numpy.log(sumP) + beta * numpy.sum(D * P) / sumP
    return H

def cal_p(D,entropy,K=50):
    beta=1.0
    H=cal_entropy(D,beta);
    error=H-entropy
    k=0
    betamin=-numpy.inf
    betamax=numpy.inf
    while numpy.abs(error)>1e-4 and k<=K:
        if error > 0:
            betamin=copy.deepcopy(beta)
            if betamax==numpy.inf:
                beta=beta*2
            else:
                beta=(beta+betamax)/2
        else:
            betamax=copy.deepcopy(beta)
            if betamin==-numpy.inf:
                beta=beta/2
            else:
                beta=(beta+betamin)/2
        H=cal_entropy(D,beta)
        error=H-entropy
        k+=1
    P=numpy.exp(-D*beta)
    return P

def cal_matrix_P(X,neighbors=30):
    entropy=numpy.log(neighbors)
    n1,n2=X.shape
    # Eucli distances
    D=numpy.square(metrics.pairwise_distances(X))
    # Use tree instead, need to improve
    D_sort=numpy.argsort(D,axis=1)
    P=numpy.zeros((n1,n1))
    for i in xrange(n1):
        Di=D[i,D_sort[i,1:]]
        P[i,D_sort[i,1:]]=cal_p(Di,entropy=entropy)
    P=P+numpy.transpose(P)
    P=P/numpy.sum(P)
    # early exaggeration
    P=P*4
    P=numpy.maximum(P,1e-12)
    return P

def cal_gradients(P,Q,Y):
    n1,n2=Y.shape
    DC=numpy.zeros((n1,n2))
    for i in xrange(n1):
        E=(1+numpy.sum((Y[i,:]-Y)**2,axis=1))**(-1)
        F=Y[i,:]-Y
        G=(P[i,:]-Q[i,:])
        E=E.reshape((-1,1))
        G=G.reshape((-1,1))
        G=numpy.tile(G,(1,n2))
        E=numpy.tile(E,(1,n2))
        # print E.shape,F.shape,G.shape,DC[i,:].shape
        DC[i,:]=numpy.sum(4*G*E*F,axis=0)
        # for j in xrange(n1):
        #    DC[i,:]=DC[i,:]+4*(P[i,j]-Q[i,j])*(1+numpy.sum((Y[i,:]-Y[j,:])**2))**(-1)*(Y[i,:]-Y[j,:])
    return DC


def tsne(X,n=2,neighbors=30,max_iter=200):
    n1,n2=X.shape
    P=cal_matrix_P(X,neighbors)
    # Random initial Or MDS initial
    Y=numpy.random.randn(n1,n)*1e-4
    A=10.0
    B=5.0
    for i  in xrange(max_iter):
        sum_Y = numpy.sum(numpy.square(Y), 1)
        num = 1 / (1 + numpy.add(numpy.add(-2 * numpy.dot(Y, Y.T), sum_Y).T, sum_Y))
        num[range(n1), range(n1)] = 0
        Q = num / numpy.sum(num)
        Q = numpy.maximum(Q, 1e-12)
        DY=cal_gradients(P,Q,Y)
        if i==0:
            Y=Y-A*DY
            Y1=Y
        elif i==1:
            Y=Y-A*DY
            Y2=Y
        else:
            Y=Y-A*DY+(B/i)*(Y2-Y1)
            Y1=Y2
            Y2=Y
            if cal_loss(P,Q)<1e-3:
                return Y
        if numpy.fmod(i+1,10)==0:
            print '%s iterations the error is %s'%(str(i+1),str(round(cal_loss(P,Q),2)))
##        if i==100:
##            P=P/4
    return Y



def test_iris():
    data=datasets.load_iris()
    X=data.data
    target=data.target
    t1=time.time()
    Y=tsne(X,n=2,max_iter=300)
    t2=time.time()
    print "Custom TSNE cost time: %s"%str(round(t2-t1,2))
    figure1=pyplot.figure()
    pyplot.subplot(1,2,1)
    pyplot.plot(Y[0:50,0],Y[0:50,1],'ro',markersize=30)
    pyplot.plot(Y[50:100,0],Y[50:100,1],'gx',markersize=30)
    pyplot.plot(Y[100:150,0],Y[100:150,1],'b*',markersize=30)
    pyplot.title('CUSTOM')
    pyplot.subplot(1,2,2)
    t1=time.time()
    Y1=manifold.TSNE(2).fit_transform(data.data)
    t2=time.time()
    print "Sklearn TSNE cost time: %s"%str(round(t2-t1,2))
    pyplot.plot(Y1[0:50,0],Y1[0:50,1],'ro',markersize=30)
    pyplot.plot(Y1[50:100,0],Y1[50:100,1],'gx',markersize=30)
    pyplot.plot(Y1[100:150,0],Y1[100:150,1],'b*',markersize=30)
    pyplot.title('SKLEARN')
    pyplot.show()

def test_digits():
    data=datasets.load_digits()
    X=data.data
    target=data.target
    t1=time.time()
    Y=tsne(X,n=2,max_iter=100)
    t2=time.time()
    t=t2-t1
    print "Custom TSNE cost time: %s"%str(round(t,2))
    figure1=pyplot.figure()
    pyplot.subplot(1,2,1)
    for i in range(10):
        xxx1 = Y[target == i, 0]
        xxx2 = Y[target == i, 1]
        pyplot.scatter(xxx1,xxx2,c=color[i])
    pyplot.xlim(numpy.min(Y)-5,numpy.max(Y)+5)
    pyplot.xlim(numpy.min(Y)-5,numpy.max(Y)+5)
    pyplot.title('CUSTOM: %ss'%str(round(t,2)))
    pyplot.subplot(1,2,2)
    t1=time.time()
    Y1=manifold.TSNE(2).fit_transform(data.data)
    t2=time.time()
    t=t2-t1
    print "Sklearn TSNE cost time: %s"%str(round(t,2))
    for i in range(10):
        xxx1 = Y1[target == i, 0]
        xxx2 = Y1[target == i, 1]
        pyplot.scatter(xxx1,xxx2,c=color[i])
    pyplot.xlim(numpy.min(Y1)-5,numpy.max(Y1)+5)
    pyplot.xlim(numpy.min(Y1)-5,numpy.max(Y1)+5)
    pyplot.title('SKLEARN: %ss'%str(round(t,2)))
    pyplot.show()

color=['yellow','black','green','red','blue','orange','brown','pink','purple','grey']


if __name__ == "__main__":
    test_iris()
    # test_digits()
