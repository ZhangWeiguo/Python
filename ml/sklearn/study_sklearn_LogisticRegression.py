#-*- encoding:utf-8-*-
import pandas
from sklearn import datasets
import numpy
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report

data=datasets.load_breast_cancer()
Data=pandas.DataFrame(data=data.data,columns=data.feature_names)
Data['target']=data.target

# 描述
print Data.describe()
print Data.count()

# 替换缺失值
Data=Data.fillna(0)
# value=0/ or dict
# axis=0/1
# method='bfill'/'ffill'

# 删除缺失值样本
Data=Data.dropna(axis=0,how='any')
# axis=0/1
# how='any'/'all'
# thresh= int (the number of the null)

# 计数
print Data.count()

# 替换掉特殊值
# Data=Data.replace(to_replace='?', value=numpy.nan)
# Data=Data.repacel(to_replace=[0,1,2],value=[1,2,3])


# 数据集拆分
x_train,x_test,y_train,y_test=train_test_split(Data.ix[:,data.feature_names],Data.ix[:,'target'],test_size=0.25,random_state=33)


# 模型训练及检验
cf1=LogisticRegression()
cf1.fit(x_train,y_train)
y_test_pre1=cf1.predict(x_test)
score1=cf1.score(x_test,y_test)

cf2=SGDClassifier()
cf2.fit(x_train,y_train)
y_test_pre2=cf2.predict(x_test)
score2=cf2.score(x_test,y_test)

print score1
print score2

print classification_report(y_test,y_test_pre1,target_names=data.target_names)
print classification_report(y_test,y_test_pre2,target_names=data.target_names)





