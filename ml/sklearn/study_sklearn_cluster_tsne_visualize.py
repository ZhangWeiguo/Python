# -*-encoding:utf-8-*-
from sklearn import manifold
from sklearn import decomposition
from sklearn import datasets
from sklearn import svm
from sklearn.preprocessing import scale,MinMaxScaler
from matplotlib import pyplot,colors
import numpy,pandas
from pandas.tools import plotting
from pylab import mpl
mpl.rcParams['axes.unicode_minus']=False
mpl.rcParams['font.sans-serif']=['SimHei']

from moviepy.video.io.bindings import mplfig_to_npimage as figage
import moviepy.editor as mpe
import shelve

# data get
data=datasets.load_digits()
x=data.data
y=data.target

# data standard
stand=MinMaxScaler((0,5))
x=stand.fit_transform(x)

# color list
'''
color=[]
for i in colors.cnames:
    color.append(i)
'''
color=['yellow','black','green','red','blue','orange','brown','pink','purple','grey']


def make_frame(t):
    print 'begin'
    tt=int(t/0.05+1)
    # print tt
    pyplot.clf()
    for i in range(10):
        xxx1 = XX[tt][YY == i, 0]
        xxx2 = XX[tt][YY == i, 1]
        #print xxx1.shape,xxx2.shape
        pyplot.scatter(xxx1,xxx2,c=color[i])
    pyplot.title('T-SNE降维'.decode('utf-8', 'ignore'))
    pyplot.xlim(-100, 100)
    pyplot.ylim(-100, 100)
    print 'end'
    return figage(figure1)
    
    
DD=shelve.open('tsne.dat')
XX=DD['tsne']
YY=DD['target']
DD.close()
figure1=pyplot.figure('TSNE VISUALIZING DYNAMIC',dpi=600)
pyplot.xlabel('component(1)')
pyplot.ylabel('component(2)')
for i in range(10):
    xxx1 = XX[0][YY == i, 0]
    xxx2 = XX[0][YY == i, 1]
    pyplot.scatter(xxx1,xxx2,c=color[i])
    #print xxx1.shape,xxx2.shape
    pyplot.xlim(-100,100)
    pyplot.ylim(-100,100)
picture=mpe.VideoClip(make_frame,duration=50)
picture.write_videofile("a.mp4",codec='mpeg4',fps=20)







def static_visualize(x,y):
    tsne=manifold.TSNE(n_components=2)
    x2=tsne.fit_transform(x)

    cf=svm.NuSVC(degree=5)
    cf.fit(x2,y)
    xx1=numpy.linspace(numpy.min(x2)-1,numpy.max(x2)+1,100)
    xx2=xx1
    xx1,xx2=numpy.meshgrid(xx1,xx2)
    xx1=xx1.reshape((100**2,1))
    xx2=xx2.reshape((100**2,1))
    yy=cf.predict(numpy.c_[xx1,xx2])
    xx1=xx1.reshape((100,100))
    xx2=xx2.reshape((100,100))
    yy=yy.reshape((100,100))

    figure4=pyplot.figure(4,figsize=(25, 20))
    pyplot.subplot(1,2,1)
    for i in range(10):
        xxx1 = x2[y == i, 0]
        xxx2 = x2[y == i, 1]
        for j in range(len(xx1)):
            print i, j
            pyplot.text(xxx1[j], xxx2[j], str(i),
                        color=color[i],
                        fontdict={'weight': 'bold', 'size': 13})
    pyplot.title('T-SNE降维'.decode('utf-8', 'ignore'))
    pyplot.xlim(numpy.min(x2) - 1, numpy.max(x2) + 1)
    pyplot.ylim(numpy.min(x2) - 1, numpy.max(x2) + 1)


    pyplot.subplot(1,2,2)
    pyplot.contourf(xx1, xx2, yy)
    for i in range(10):
        xxx1=x2[y==i,0]
        xxx2=x2[y==i,1]
        for j in range(len(xx1)):
            print i,j
            pyplot.text(xxx1[j], xxx2[j], str(i),
                     color=color[i],
                     fontdict={'weight': 'bold', 'size': 13})
    pyplot.title('SVM分类'.decode('utf-8','ignore'))
    pyplot.xlim(numpy.min(x2)-1,numpy.max(x2)+1)
    pyplot.ylim(numpy.min(x2)-1,numpy.max(x2)+1)
    pyplot.show()








