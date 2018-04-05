# -*-encoding：gbk -*-
'''
created by zwg in 2017-03-14
'''

from sklearn import cluster
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot
import numpy
from sklearn.metrics import adjusted_rand_score # 聚类效果和标准分类的比较
from sklearn.metrics import silhouette_score

#data=datasets.make_blobs(n_samples=500,n_features=2,centers=[[-1,0],[0,1],[1,0]],random_state=1)
#x=data[0]
#y=data[1]

data=datasets.load_iris()
x=data.data[:,0:2]
y=data.target

stand=StandardScaler()
x=stand.fit_transform(x)

clu=cluster.KMeans(n_clusters=3)
'''
n_clusters=8,init='k-means++',
n_init=10, max_iter=300,
tol=0.0001, precompute_distances='auto',
verbose=0, random_state=None,
copy_x=True, n_jobs=1,
algorithm='auto')
http://scikit-learn.org/dev/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans
'''
clu.fit(x)
print '聚类效果和标准效果比较得分：%f'% adjusted_rand_score(y,clu.labels_)
print '聚类效果的轮廓系数得分：%f'% silhouette_score(x,clu.labels_)
centers=clu.cluster_centers_



n=100
xx1=numpy.linspace(numpy.min(x[:,0])-1,numpy.max(x[:,0])+1,n)
xx2=numpy.linspace(numpy.min(x[:,1])-1,numpy.max(x[:,1])+1,n)
xx1,xx2=numpy.meshgrid(xx1,xx2)
xx1=xx1.reshape((n**2,1))
xx2=xx2.reshape((n**2,1))
yy=clu.predict(numpy.c_[xx1,xx2])
xx1=xx1.reshape((n,n))
xx2=xx2.reshape((n,n))
yy=yy.reshape((n,n))



figure=pyplot.figure()
pyplot.subplot(1,2,1)
pyplot.scatter(x[y==0,0],x[y==0,1],color='red',label='The First Kind',s=13)
pyplot.scatter(x[y==1,0],x[y==1,1],color='green',label='The Second Kind',s=13)
pyplot.scatter(x[y==2,0],x[y==2,1],color='yellow',label='The Third Kind',s=13)
pyplot.legend()
pyplot.subplot(1,2,2)
pyplot.plot(x[y==0,0],x[y==0,1],'k+',markersize=10)
pyplot.plot(x[y==1,0],x[y==1,1],'ko',markersize=5)
pyplot.plot(x[y==2,0],x[y==2,1],'k*',markersize=10)
pyplot.contourf(xx1,xx2,yy)
pyplot.scatter(centers[:,0],centers[:,1],color='white',marker='x',s=100)
pyplot.show()



