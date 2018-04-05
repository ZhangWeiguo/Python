# -*-encoding:utf-8 -*-
'''
create table by zwg in 2017-03-13
'''


from sklearn import datasets
from sklearn import neural_network
from sklearn.cross_validation import train_test_split
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.metrics import classification_report

# 拟合
data=datasets.load_breast_cancer()
x=data.data
y=data.target
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=33)
cf=neural_network.MLPRegressor(hidden_layer_sizes=(100,100,100,100),max_iter=5000)
cf.fit(x_train,y_train)
y_test_pre=cf.predict(x_test)
print 'The Normal socre of the nn is : %f'% cf.score(x_test,y_test)
print 'The R-squared score of the nn is : %f'% r2_score(y_test,y_test_pre)
print 'The Mean-absolute socre of the nn is : %f'% mean_absolute_error(y_test,y_test_pre)
print 'Thr Mean-squared score of the nn is : %f'% mean_squared_error(y_test,y_test_pre)



#分类
data1=datasets.load_iris()
x1=data1.data
y1=data1.target
x1_train,x1_test,y1_train,y1_test=train_test_split(x1,y1,test_size=0.25,random_state=33)
cf1=neural_network.MLPClassifier()
cf1.fit(x1_train,y1_train)
y1_test_pre=cf1.predict(x1_test)
print classification_report(y1_test,y1_test_pre,target_names=data1.target_names)




