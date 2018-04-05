# -*-encoding:utf-8 -*-
from time import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D as ax3
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits,fetch_olivetti_faces,load_digits

from sklearn.decomposition import PCA
from sklearn.preprocessing import scale,StandardScaler
from sklearn import decomposition
from pylab import mpl
mpl.rcParams['font.sans-serif']=['SimHei']
mpl.rcParams['axes.unicode_minus']=False



color=['red','purple','yellow']
for i in colors.cnames:
    if i in color:
        pass
    else:
        color.append(i)


    
def generate_circle_data1():
    xx=np.zeros((1500,3))
    x1=np.ones((500,))+0.5*np.random.rand(500)-0.5
    r1=np.linspace(0,6*np.pi,500)
    r2=np.linspace(0,6*np.pi,500)
    xx[0:500,0]=x1*np.sin(r1)*np.sin(r2)
    xx[0:500,1]=x1*np.cos(r1)*np.sin(r2)
    xx[0:500,2]=x1*np.cos(r2)
    x1=3*np.ones((500,))+0.6*np.random.rand(500)-0.6
    xx[500:1000,0]=x1*np.sin(r1)*np.sin(r2)
    xx[500:1000,1]=x1*np.cos(r1)*np.sin(r2)
    xx[500:1000,2]=x1*np.cos(r2)
    x1=6*np.ones((500,))+1.1*np.random.rand(500)-0.6
    xx[1000:1500,0]=x1*np.sin(r1)*np.sin(r2)
    xx[1000:1500,1]=x1*np.cos(r1)*np.sin(r2)
    xx[1000:1500,2]=x1*np.cos(r2)
    target=np.zeros((1500,))
    target[0:500]=0
    target[500:1000]=1
    target[1000:1500]=2
    target=target.astype('int')
    return xx,target

    
def generate_circle_data2():
    xx=np.zeros((1500,3))
    x1=np.ones((500,))+0.5*np.random.rand(500)-0.5
    r1=np.linspace(0,2*np.pi,500)
    r2=np.linspace(0,np.pi,500)
    xx[0:500,0]=x1*np.sin(r1)*np.sin(r2)
    xx[0:500,1]=x1*np.cos(r1)*np.sin(r2)
    xx[0:500,2]=x1*np.cos(r2)
    x1=3*np.ones((500,))+0.6*np.random.rand(500)-0.6
    xx[500:1000,0]=x1*np.sin(r1)*np.sin(r2)
    xx[500:1000,1]=x1*np.cos(r1)*np.sin(r2)
    xx[500:1000,2]=x1*np.cos(r2)
    x1=6*np.ones((500,))+1.1*np.random.rand(500)-0.6
    xx[1000:1500,0]=x1*np.sin(r1)*np.sin(r2)
    xx[1000:1500,1]=x1*np.cos(r1)*np.sin(r2)
    xx[1000:1500,2]=x1*np.cos(r2)
    target=np.zeros((1500,))
    target[0:500]=0
    target[500:1000]=1
    target[1000:1500]=2
    target=target.astype('int')
    return xx,target


def generate_circle_data3():
    xx=np.zeros((2700,3))
    x1=np.ones((900,))+0.5*np.random.rand(900)-0.5
    r1=np.linspace(0,2*np.pi,30)
    r2=np.linspace(0,np.pi,30)
    r1,r2=np.meshgrid(r1,r2)
    r1=r1.ravel()
    r2=r2.ravel()
    xx[0:900,0]=x1*np.sin(r1)*np.sin(r2)
    xx[0:900,1]=x1*np.cos(r1)*np.sin(r2)
    xx[0:900,2]=x1*np.cos(r2)
    x1=3*np.ones((900,))+0.6*np.random.rand(900)-0.6
    xx[900:1800,0]=x1*np.sin(r1)*np.sin(r2)
    xx[900:1800,1]=x1*np.cos(r1)*np.sin(r2)
    xx[900:1800,2]=x1*np.cos(r2)
    x1=6*np.ones((900,))+1.1*np.random.rand(900)-0.6
    xx[1800:2700,0]=x1*np.sin(r1)*np.sin(r2)
    xx[1800:2700,1]=x1*np.cos(r1)*np.sin(r2)
    xx[1800:2700,2]=x1*np.cos(r2)
    target=np.zeros((2700,))
    target[0:900]=0
    target[900:1800]=1
    target[1800:2700]=2
    target=target.astype('int')
    return xx,target  

def compare_KPCA():
    data,target=generate_circle_data2()
    pca=decomposition.PCA(n_components=2)
    data1=pca.fit_transform(data)
    try:
        figure1=plt.figure(1)
        ax=ax3(figure1)
        ax.scatter3D(data[:,0],data[:,1],data[:,2],c=[color[i] for i in target],alpha=0.5)
        plt.title('Origin Data')
    except:
        pass
    
    figure2=plt.figure(2)
    k=1
    for kernel in ['linear','rbf','poly','sigmoid']:
        plt.subplot(1,4,k)
        k+=1
        kpca=decomposition.KernelPCA(n_components=2,kernel=kernel)
        data2=kpca.fit_transform(data)
        plt.scatter(data2[:,0],data2[:,1],c=[color[i] for i in target])
        plt.title(kernel)
    plt.suptitle('The Comparasion Between KPCA')
    plt.show()





def bench_k_means(estimator, name, data,labels):
    t0 = time()
    estimator.fit(data)
    print('%-9s\t%.2fs\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean')))

# Kmeans directly compared to Kmeans after pca 
def compare_Kmeans_PCA():
    np.random.seed(42)
    digits = load_digits()
    #data = scale(digits.data)  #standrad
    stand=StandardScaler()
    data = stand.fit_transform(digits.data)
    n_samples, n_features = data.shape
    n_digits = len(np.unique(digits.target))
    labels = digits.target
    sample_size = 300
    print("n_digits: %d, \t n_samples %d, \t n_features %d"% (n_digits, n_samples, n_features))
    print(82 * '_')
    print('init\t\ttime\tinertia\thomo\tcompl\tv-meas\tARI\tAMI\tsilhouette')
    bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=data,labels=labels)
    bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
                  name="k-means-random", data=data,labels=labels)
    pca = PCA(n_components=n_digits).fit(data)
    bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
                  name="PCA-based",
                  data=data,labels=labels)
    print(82 * '_')
    reduced_data = PCA(n_components=2).fit_transform(data)
    kmeans = KMeans(init='k-means++', n_clusters=n_digits, n_init=10)
    kmeans.fit(reduced_data)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .02     # point in the mesh [x_min, x_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    plt.show()



#compare_Kmeans_PCA()
compare_KPCA()


