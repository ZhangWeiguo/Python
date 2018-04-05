# -*- encoding:utf-8 -*-
from sklearn import datasets
from sklearn import naive_bayes
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report
import numpy
data=datasets.load_iris()
x = data.data
y = data.target
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=10)

# cf=naive_bayes.MultinomialNB()  #多项式分布，实际就是泊松分布
cf=naive_bayes.GaussianNB()         #高斯分布，最常见的的
# cf=naive_bayes.BernoulliNB()      #泊松分布

#cf.fit(x_train,y_train,classes=numpy.unique(y_train))
cf.partial_fit(x_train,y_train,classes=numpy.unique(y_train))#分块训练


y_test_pre=cf.predict(x_test)
print cf.score(x_test,y_test)
print classification_report(y_test,y_test_pre,target_names=data.target_names)
