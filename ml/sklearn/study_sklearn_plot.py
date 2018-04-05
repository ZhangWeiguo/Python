from sklearn import datasets
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn import tree
import sklearn
from matplotlib import pyplot
import numpy
from sklearn import svm
data=datasets.load_iris()
x=data.data[:,0:2]
y=data.target
target_names=data.target_names
feature_names=data.feature_names
stand=sklearn.preprocessing.StandardScaler()
xs=stand.fit_transform(x)
#cf=tree.DecisionTreeClassifier()
cf=svm.LinearSVC()
cf.fit(xs,y)
y_pre=cf.predict(xs)

xx1=numpy.linspace(numpy.min(xs[:,0])-1,numpy.max(xs[:,0])+1,100)
xx2=numpy.linspace(numpy.min(xs[:,1])-1,numpy.max(xs[:,1])+1,100)

n,=xx1.shape
print n
[xx1,xx2]=numpy.meshgrid(xx1,xx2)
print xx1.shape
xx1=xx1.reshape((n**2,1))
xx2=xx2.reshape((n**2,1))


xx=numpy.c_[xx1,xx2]
yy=cf.predict(xx)
yy=yy.reshape((n,n))
xx1=xx1.reshape((n,n))
xx2=xx2.reshape((n,n))

figure=pyplot.figure()

pyplot.plot(xs[y_pre==0,0],xs[y_pre==0,1],'ro',markersize=5,label=target_names[0])
pyplot.plot(xs[y_pre==1,0],xs[y_pre==1,1],'go',markersize=5,label=target_names[1])
pyplot.plot(xs[y_pre==2,0],xs[y_pre==2,1],'yo',markersize=5,label=target_names[1])
pyplot.xlabel(feature_names[0])
pyplot.ylabel(feature_names[1])
pyplot.contourf(xx1,xx2,yy)


pyplot.legend()
pyplot.show()
