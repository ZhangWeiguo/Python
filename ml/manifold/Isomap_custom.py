import numpy
from sklearn import metrics,datasets,manifold,preprocessing
from scipy import optimize
from matplotlib import pyplot
import pandas
import collections
from mpl_toolkits.mplot3d import Axes3D
def generate_circle_data():
    xx=numpy.zeros((1200,3))
    x1=numpy.ones((400,))+0.5*numpy.random.rand(400)-0.5
    r1=numpy.linspace(0,2*numpy.pi,20)
    r2=numpy.linspace(0,numpy.pi,20)
    r1,r2=numpy.meshgrid(r1,r2)
    r1=r1.ravel()
    r2=r2.ravel()
    xx[0:400,0]=x1*numpy.sin(r1)*numpy.sin(r2)
    xx[0:400,1]=x1*numpy.cos(r1)*numpy.sin(r2)
    xx[0:400,2]=x1*numpy.cos(r2)
    x1=3*numpy.ones((400,))+0.6*numpy.random.rand(400)-0.6
    xx[400:800,0]=x1*numpy.sin(r1)*numpy.sin(r2)
    xx[400:800,1]=x1*numpy.cos(r1)*numpy.sin(r2)
    xx[400:800,2]=x1*numpy.cos(r2)
    x1=6*numpy.ones((400,))+1.1*numpy.random.rand(400)-0.6
    xx[800:1200,0]=x1*numpy.sin(r1)*numpy.sin(r2)
    xx[800:1200,1]=x1*numpy.cos(r1)*numpy.sin(r2)
    xx[800:1200,2]=x1*numpy.cos(r2)
    target=numpy.zeros((1200,))
    target[0:400]=0
    target[400:800]=1
    target[800:1200]=2
    target=target.astype('int')
    return xx,target

def generate_curve_data():
    xx,target=datasets.samples_generator.make_s_curve(400, random_state=9)
    return xx,target

def floyd(D,n_neighbors=15):
    Max=numpy.max(D)*1000
    n1,n2=D.shape
    k=n_neighbors
    D1=numpy.ones((n1,n1))*Max
    D_arg=numpy.argsort(D,axis=1)
    for i in range(n1):
        D1[i,D_arg[i,0:k+1]]=D[i,D_arg[i,0:k+1]]
    for k in xrange(n1):
        for i in xrange(n1):
            for j in xrange(n1):
                if D1[i,k]+D1[k,j]<D1[i,j]:
                    D1[i,j]=D1[i,k]+D1[k,j]
    return D1
    


def calculate_distance(x,y):
    d=numpy.sqrt(numpy.sum((x-y)**2))
    return d
def calculate_distance_matrix(x,y):
    d=metrics.pairwise_distances(x,y)
    return d
def cal_B(D):
    (n1,n2)=D.shape
    DD=numpy.square(D)
    Di=numpy.sum(DD,axis=1)/n1
    Dj=numpy.sum(DD,axis=0)/n1
    Dij=numpy.sum(DD)/(n1**2)
    B=numpy.zeros((n1,n1))
    for i in xrange(n1):
        for j in xrange(n2):
            B[i,j]=(Dij+DD[i,j]-Di[i]-Dj[j])/(-2)
    return B
    

def MDS(data,n=2):
    D=calculate_distance_matrix(data,data)
    B=cal_B(D)
    Be,Bv=numpy.linalg.eigh(B)
    Be_sort=numpy.argsort(-Be)
    Be=Be[Be_sort]
    Bv=Bv[:,Be_sort]
    Bez=numpy.diag(Be[0:n])
    Bvz=Bv[:,0:n]
    Z=numpy.dot(numpy.sqrt(Bez),Bvz.T).T
    return Z


def Isomap(data,n=2,n_neighbors=30):
    D=calculate_distance_matrix(data,data)
    D_floyd=floyd(D)
    B=cal_B(D_floyd)
    Be,Bv=numpy.linalg.eigh(B)
    Be_sort=numpy.argsort(-Be)
    Be=Be[Be_sort]
    Bv=Bv[:,Be_sort]
    Bez=numpy.diag(Be[0:n])
    Bvz=Bv[:,0:n]
    Z=numpy.dot(numpy.sqrt(Bez),Bvz.T).T
    return Z


if __name__=='__main__':
    data,target=generate_curve_data()

    figure1=pyplot.figure()
    ax=Axes3D(figure1)
    ax.scatter3D(data[:,0],data[:,1],data[:,2],c=preprocessing.scale(target))
    ax.set_axis_on()
    pyplot.show()

    Z_Isomap=Isomap(data,n=2)
    Z_MDS=MDS(data)



    figure=pyplot.figure()
    pyplot.suptitle('ISOMAP COMPARE TO MDS')
    pyplot.subplot(1,2,1)
    pyplot.title('ISOMAP')
    pyplot.scatter(Z_Isomap[:,0],Z_Isomap[:,1],c=target,s=60)
    pyplot.subplot(1,2,2)
    pyplot.title('MDS')
    pyplot.scatter(Z_MDS[:,0],Z_MDS[:,1],c=target,s=60)
    pyplot.show()



