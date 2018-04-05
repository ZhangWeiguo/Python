#-*-encoding:utf-8-*-
'''
created by zwg in 2017-03-04
'''


from sklearn import tree
from sklearn import datasets
import numpy,pandas
from sklearn.externals.six import StringIO
import os,pydot


def fun1():
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    from sklearn.tree import DecisionTreeClassifier
    # Parameters
    n_classes = 3
    plot_colors = "bry"
    plot_step = 0.02
    # Load data
    iris = load_iris()
    for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
                                    [1, 2], [1, 3], [2, 3]]):
        # We only take the two corresponding features
        X = iris.data[:, pair]
        y = iris.target

        # Shuffle
        idx = np.arange(X.shape[0])
        np.random.seed(13)
        np.random.shuffle(idx)
        X = X[idx]
        y = y[idx]

        # Standardize
        mean = X.mean(axis=0)
        std = X.std(axis=0)
        X = (X - mean) / std

        # Train
        clf = DecisionTreeClassifier().fit(X, y)

        # Plot the decision boundary
        plt.subplot(2, 3, pairidx + 1)

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                             np.arange(y_min, y_max, plot_step))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        numpy.ufunc
        cs = plt.contourf(xx, yy, Z)

        plt.xlabel(iris.feature_names[pair[0]])
        plt.ylabel(iris.feature_names[pair[1]])
        plt.axis("tight")

        # Plot the training points
        for i, color in zip(range(n_classes), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                        cmap=plt.cm.Paired)

        plt.axis("tight")

    plt.suptitle("Decision surface of a decision tree using paired features")
    plt.legend()
    plt.show()

def fun2():
    data = datasets.load_breast_cancer()
    x1 = data.data
    y1 = data.target
    features = data.feature_names
    targets = data.target_names

    random_sample=range(569)
    numpy.random.shuffle(random_sample)
    print x1.shape
    x=x1[random_sample[0:300],:]
    y=y1[random_sample[0:300]]
    xx=x1[random_sample[300:569],:]
    yy=y1[random_sample[300:569]]


    cf = tree.DecisionTreeClassifier(criterion='entropy',min_samples_split=2)
    # 一些重要的参数列表
    # criterion = 'gini' / 'entropy'
    # spliter = 'best' / 'random'
    # max_features = int  随机选择spliter时的范围界限
    # max_depth = int
    # min_samples_split = default 2
    # min_samples_leaf int = (default 1)
    # class_weight = dictionary ( and list of dictionary for 多输出问题 )
    # max_leaf_nodes

    cf.fit(x, y)
    print cf.score(xx,yy)
    # tree的可视化
    # dot_data = StringIO()
    # tree.export_graphviz(cf, out_file=dot_data, feature_names=data.feature_names,
    #                      class_names=data.target_names,
    #                      filled=True,
    #                      rounded=True)
    # graph1 = pydot.graph_from_dot_data(dot_data.getvalue())
    # for i in graph1:
    #     i.write_pdf('tree.pdf')

def generate_tree_pdf(cf,feature_names,class_names,filename):
    dot_data = StringIO()
    tree.export_graphviz(cf, out_file=dot_data, feature_names=feature_names,
                      class_names=target_names,
                      filled=True,
                      rounded=True)
    graph1 = pydot.graph_from_dot_data(dot_data.getvalue())
    for i in graph1:
        i.write_pdf(filename)
    




if __name__=='__main__':
    fun1()

