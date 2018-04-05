# -*- encoding:utf-8 -*-
from sklearn import datasets
from matplotlib import pyplot
import numpy

# 两个环形数据
data1=datasets.make_circles(n_samples=500,noise=0.05)
'''
n_samples : int, optional (default=100)
The total number of points generated.
shuffle : bool, optional (default=True)
Whether to shuffle the samples.
noise : double or None (default=None)
Standard deviation of Gaussian noise added to the data.
factor : double < 1 (default=.8)
Scale factor between inner and outer circle.
'''
x1=data1[0]
y1=data1[1]

# 多个分类数据
data2=datasets.make_classification(n_samples=500,n_features=4,
                                   n_informative=2,n_redundant=0,n_classes=3,
                                   n_clusters_per_class=1,random_state=33)
'''
n_samples=100,n_features=20,
n_informative=2,n_redundant=2,
n_repeated=0,n_classes=2,
n_clusters_per_class=2, weights=None,
flip_y=0.01, class_sep=1.0,
hypercube=True, shift=0.0,
scale=1.0, shuffle=True,
random_state=None
'''
x2=data2[0]
y2=data2[1]


# FridMan函数
'''
y(X) =
10 * sin(pi * X[:, 0] * X[:, 1]) +
20 * (X[:, 2] - 0.5) ** 2 +
10 * X[:, 3] +
5 * X[:, 4] +
noise * N(0, 1).
'''
data3=datasets.make_friedman1(n_samples=200,n_features=5,noise=0.01)
x3=numpy.linspace(-10,10,300)
y3=10 * numpy.sin(numpy.pi * x3)+ 5* numpy.cos(x3)+2* numpy.sin(2*x3)+numpy.random.rand(300)*2


# 聚类数据
data4=datasets.make_blobs(n_samples=200,n_features=2,centers=[[0,0],[1,1],[1,-1]],random_state=33)
x4=data4[0]
y4=data4[1]


figure=pyplot.figure()
pyplot.suptitle('Datasets Make Data')
pyplot.subplot(2,2,1)
pyplot.title('Make Two Circles')
pyplot.plot(x1[y1==0,0],x1[y1==0,1],'ro')
pyplot.plot(x1[y1==1,0],x1[y1==1,1],'go')
pyplot.subplot(2,2,2)
pyplot.plot(x2[y2==0,0],x2[y2==0,1],'ro')
pyplot.plot(x2[y2==1,0],x2[y2==1,1],'go')
pyplot.plot(x2[y2==2,0],x2[y2==2,1],'bo')
pyplot.title('Make Three Classes')
pyplot.subplot(2,2,3)
pyplot.title('Make FriedMan Function 5D')
pyplot.scatter(x3,y3)
pyplot.subplot(2,2,4)
pyplot.plot(x4[y4==0,0],x4[y4==0,1],'ro')
pyplot.plot(x4[y4==1,0],x4[y4==1,1],'go')
pyplot.plot(x4[y4==2,0],x4[y4==2,1],'bo')
pyplot.title('Make Cluster Data')
pyplot.show()

