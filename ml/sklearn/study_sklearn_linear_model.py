#-*-encoding:utf-8-*-
'''
created by zwg in 2017-03-04
'''


import numpy
from sklearn import datasets
import pandas
from sklearn import linear_model
from pandas.tools.plotting import scatter_matrix
import pylab

if __name__=='__main__':
    data=datasets.load_iris()
    columns=data.feature_names
    target=data.target_names
    x=data.data
    y=data.target

    Data=pandas.DataFrame(data=x,columns=columns)
    Data['classi']=[target[i] for i in y]
    Data['classj']=y
    color=['r','g','b']
    scatter_matrix(Data.ix[:,0:4],c=[color[i] for i in y])
    pylab.show()

    # ���Իع�
    x1=Data[Data.classj==0].ix[:,0:1]
    y1=Data[Data.classj==0].ix[:,1:2]
    print '%s��%s�����ϵ����%s'%(columns[0],columns[1],
                           str(numpy.corrcoef(x1,y1,rowvar=False)[0,1]))
    cf1=linear_model.LinearRegression()
    cf1.fit(x1,y1)
    print '�÷�Ϊ��%s'%str(cf1.score(x1,y1))

    #logistic �ع�
    x2=Data.ix[:,0:4]
    y2=Data.ix[:,5]
    cf2=linear_model.LogisticRegression()
    cf2.fit(x2,y2)
    print '�÷�Ϊ��%s'%str(cf2.score(x2,y2))
    print 'ϵ��Ϊ��'
    print cf2.coef_
    print cf2.intercept_


def lasco():
    # Lasco �ع�
    import time
    from sklearn import linear_model as lm
    import numpy
    x = numpy.random.rand(100, 2)
    y = 0.2 * x[:, 0] + x[:, 1] * 0.1 + 1
    t0 = time.time()
    clf = lm.Lasso()  # Ĭ��alpha=1
    clf.fit(x, y)
    t1 = time.time()
    print 'Ĭ��alpha=1�µ�ƽ����������ʱ�䣺', \
        numpy.mean(numpy.abs(clf.predict(x) - y)), t1 - t0
    clf_lasso1 = lm.LassoCV()
    clf_lasso1.fit(x, y)
    t2 = time.time()
    print 'CV������֤alpha�µ�ƽ����������ʱ�䣺', \
        numpy.mean(numpy.abs(clf_lasso1.predict(x) - y)), t2 - t1
    clf_lasso2 = lm.LassoLarsIC(criterion='aic')
    clf_lasso2.fit(x, y)
    t3 = time.time()
    print 'AIC��֤alpha�µ�ƽ����������ʱ�䣺', \
        numpy.mean(numpy.abs(clf_lasso2.predict(x) - y)), t3 - t2
    clf_lasso3 = lm.LassoLarsIC(criterion='bic')
    clf_lasso3.fit(x, y)
    t4 = time.time()
    print 'BIC��֤alpha�µ�ƽ����������ʱ�䣺', \
        numpy.mean(numpy.abs(clf_lasso3.predict(x) - y)), t4 - t3
    clf_lasso4 = lm.LassoLarsCV()
    clf_lasso4.fit(x, y)
    t5 = time.time()
    print 'CV������֤+lars��alpha�µ�ƽ����������ʱ�䣺', \
        numpy.mean(numpy.abs(clf_lasso4.predict(x) - y)), t5 - t4

def ridge():
    # ��ع�
    from sklearn import linear_model as lm
    from matplotlib import pyplot as pl
    import numpy
    import time
    x = numpy.random.rand(100, 2)
    y = 0.2 * x[:, 0] + x[:, 1] * 0.1 + 1
    t0 = time.time()
    F1 = lm.RidgeCV()
    F1.fit(x, y)
    y1 = F1.predict(x)
    t1 = time.time()
    F2 = lm.Ridge()  # alpha=0ʱ������ͨ�Ļع�,Ĭ��alpha=1
    F2.fit(x, y)
    y2 = F1.predict(x)
    t2 = time.time()
    print 'CV������֤��ع��alpha������ʱ�䣺', F1.alpha_, numpy.mean(numpy.abs(y1 - y)), t1 - t0
    print 'һ����ع��alpha������ʱ�䣺', F2.alpha, numpy.mean(numpy.abs(y2 - y)), t2 - t1

def lars():
    # least angle regression method��LARS���ع�
    import time
    from sklearn import linear_model as lm
    import numpy
    x = numpy.random.rand(100, 2)
    y = 0.2 * x[:, 0] + x[:, 1] * 0.1 + 1
    t0 = time.time()
    clf = lm.Lars()
    clf.fit(x, y)
    t1 = time.time()
    print 'Ĭ���µ�ƽ����������ʱ�䣺', numpy.mean(numpy.abs(clf.predict(x) - y)), t1 - t0
    clf_lars1 = lm.LarsCV()
    clf_lars1.fit(x, y)
    t2 = time.time()
    print 'CV������֤alpha�µ�ƽ����������ʱ�䣺', numpy.mean(numpy.abs(clf_lars1.predict(x) - y)), t2 - t1

def ard():
    # ARD�ع�(�Զ�ȷ����ػع�)
    from sklearn import linear_model as lm
    import numpy
    import time
    t0 = time.time()
    clf = lm.ARDRegression()
    x = numpy.random.rand(100, 2)
    y = 0.2 * x[:, 0] + x[:, 1] * 0.1 + 1
    clf.fit(x, y)
    t1 = time.time()
    print 'ƽ����������ʱ�䣺', numpy.mean(numpy.abs(clf.predict(x) - y)), t1 - t0

def bayesian_ridge():
    # ��Ҷ˹��ع�
    from sklearn import linear_model as lm
    import numpy
    clf = lm.BayesianRidge()
    x = numpy.random.rand(10, 2) * 10
    y = x[:, 0] * 0.1 + x[:, 1] * 0.5 + 2
    clf.fit(x, y)
    print clf.predict([[2, 2]])
