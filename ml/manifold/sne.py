# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-03-30
'''

#   Improve t-sne : LargeVis
import numpy as numpy
import shelve,copy,time
from sklearn import metrics,decomposition,manifold
from sklearn import preprocessing,datasets
from matplotlib import pyplot
from sklearn import feature_extraction

def cal_entropy(D,beta):
    # P=numpy.exp(-(numpy.sqrt(D))*beta)
    P=numpy.exp(-D*beta)
    sumP=sum(P)
    sumP=numpy.maximum(sumP,1e-200)
    H=numpy.log(sumP) + beta * numpy.sum(D * P) / sumP
    return H


def cal_p(D,entropy,K=50):
    beta=1.0
    H=cal_entropy(D,beta)
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
    P=P/numpy.sum(P)
    return P

def cal_matrix_P(X,neighbors):
    entropy=numpy.log(neighbors)
    n1,n2=X.shape
    D=numpy.square(metrics.pairwise_distances(X))
    D_sort=numpy.argsort(D,axis=1)
    P=numpy.zeros((n1,n1))
    for i in xrange(n1):
        Di=D[i,D_sort[i,1:]]
        P[i,D_sort[i,1:]]=cal_p(Di,entropy=entropy)
    P=(P+numpy.transpose(P))/(2*n1)
    P=numpy.maximum(P,1e-30)
    return P

def cal_matrix_Q(Y):
    D=numpy.square(metrics.pairwise_distances(Y))
    Q=numpy.exp(-D)
    Q=Q/numpy.sum(Q)
    Q=numpy.maximum(Q,1e-30)
    return Q

def cal_gradients(P,Q,Y):
    n1,n2=Y.shape
    DC=numpy.zeros((n1,n2))
    for i in xrange(n1):
        F=Y[i,:]-Y
        G=(P[i,:]-Q[i,:])
        G=G.reshape((-1,1))
        G=numpy.tile(G,(1,n2))
        DC[i,:]=numpy.sum(4*G*F,axis=0)
    return DC

def cal_loss(P,Q):
    C=numpy.sum(P * numpy.log(P / Q))
    return C

def tsne(X,n=2,neighbors=30,max_iter=200):
    tsne_dat=shelve.open('tsne.dat')
    data=[]
    n1,n2=X.shape
    P=cal_matrix_P(X,neighbors)
    Y=numpy.random.randn(n1,n)*1e-4
    Q = cal_matrix_Q(Y)
    DY = cal_gradients(P, Q, Y)
    A=200.0
    B=0.1
    for i  in xrange(max_iter):
        data.append(Y)
        if i==0:
            Y=Y-A*DY
            Y1=Y
            error1=cal_loss(P,Q)
        elif i==1:
            Y=Y-A*DY
            Y2=Y
            error2=cal_loss(P,Q)
        else:
            YY=Y-A*DY+B*(Y2-Y1)
            QQ = cal_matrix_Q(YY)
            error=cal_loss(P,QQ)
            if error>error2:
                A=A*0.7
                continue
            elif (error-error2)>(error2-error1):
                A=A*1.2
            Y=YY
            error1=error2
            error2=error
            Q = QQ
            DY = cal_gradients(P, Q, Y)
            Y1=Y2
            Y2=Y
        if cal_loss(P,Q)<1e-3:
            return Y
        if numpy.fmod(i+1,10)==0:
            print '%s iterations the error is %s, A is %s'%(str(i+1),str(round(cal_loss(P,Q),2)),str(round(A,3)))
    tsne_dat['data']=data
    tsne_dat.close()
    return Y

def test_iris():
    data=datasets.load_iris()
    X=data.data
    target=data.target
    t1=time.time()
    Y=tsne(X,n=2,max_iter=300,neighbors=30)
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
    Y=tsne(X,n=2,max_iter=400,neighbors=50)
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



color=['yellow','black','green','red','blue',
       'orange','brown','pink','purple','grey',
       'gold','darkred','firebrick','blueviolet','bisque',
       'beige','aqua','cyan','coral','darkgrey']


if __name__ == "__main__":
    #test_iris()
    test_digits()