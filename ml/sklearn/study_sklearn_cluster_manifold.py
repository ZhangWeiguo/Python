# -*- encoding:utf-8 -*-
from sklearn import manifold,cluster
from sklearn import decomposition
from sklearn import datasets
from sklearn.preprocessing import scale,MinMaxScaler
from matplotlib import pyplot,colors
import numpy,pandas,time
from pandas.tools import plotting
from pylab import mpl
from sklearn.cross_validation import train_test_split
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import silhouette_score
mpl.rcParams['axes.unicode_minus']=False
mpl.rcParams['font.sans-serif']=['SimHei']

def manifold_study(learner,data,target,k,method_name):
    color = ['yellow', 'black', 'green', 'red', 'blue',
             'orange', 'brown', 'pink', 'purple', 'grey']
    x1=learner.fit_transform(data)
    figure = pyplot.figure(k)
    for i in range(10):
        pyplot.scatter(x1[y == i, 0], x1[y == i, 1], c=color[i],
                       figure=figure, label=str(i))
    pyplot.legend()
    pyplot.title(method_name)
    return x1


# data get
data=datasets.load_digits()
x=data.data
y=data.target

# data standard
stand=MinMaxScaler((0,1))
x=stand.fit_transform(x)

# color list
'''
color=[]
for i in colors.cnames:
    color.append(i)
'''
color = ['yellow', 'black', 'green', 'red', 'blue',
         'orange', 'brown', 'pink', 'purple', 'grey']



# PCA to 5 components
pca=decomposition.PCA(n_components=5).fit(x)
x1=pca.transform(x)
Data=pandas.DataFrame(data=x1)
Data['y']=y

# The visualize of digits data after pca to 5 components
figure1=pyplot.figure(1)
pyplot.title('弹簧图'.decode('utf-8','ignore'))
plotting.radviz(Data,class_column='y')
figure2=pyplot.figure(2)
pyplot.title('平行坐标图'.decode('utf-8','ignore'))
plotting.parallel_coordinates(Data,class_column='y')



# The comparision of this manifold methods
k=0
print '--'*40
print "%-20s\t%-10s\t%-10s\t%-5s\t%-5s"\
      %("Method","Method-time","KMeans-time","ARI","SihouetteScore")
print '--'*40
kmeans=cluster.KMeans(n_clusters=10,n_jobs=1)
tt1=time.time()
y_kmeans=kmeans.fit_predict(x)
tt2=time.time()
tt=tt2-tt1
ARI=adjusted_rand_score(y,y_kmeans)
Silhouette=silhouette_score(x,y_kmeans)
t=0.0
print "%-20s\t%-10s\t%-10s\t%-5s\t%-5s"\
      %('None',str(round(t,2)),str(round(tt,2)),str(round(ARI,2)),str(round(Silhouette,2)))
method_name=['PCA','MDS','T-SNE','Isomap','LocalLinearEmbeding','SpectralEmbeding']
for learner in [decomposition.PCA(n_components=2),
                manifold.MDS(n_components=2),
                manifold.TSNE(n_components=2),
                manifold.Isomap(n_components=2),
                manifold.LocallyLinearEmbedding(n_components=2),
                manifold.SpectralEmbedding(n_components=2)]:
    t1=time.time()
    x_manifold=manifold_study(learner,data=x,target=y,k=k+3,method_name=method_name[k])
    k=k+1
    t2=time.time()
    t=t2-t1
    tt1=time.time()
    y_kmeans=kmeans.fit_predict(x_manifold)
    tt2=time.time()
    tt=tt2-tt1
    ARI=adjusted_rand_score(y,y_kmeans)
    Silhouette=silhouette_score(x,y_kmeans)
    print "%-20s\t%-10s\t%-10s\t%-5s\t%-5s"\
          %(method_name[k-1],str(round(t,2)),str(round(tt,2)),str(round(ARI,2)),str(round(Silhouette,2)))
print '--'*40
pyplot.show()
