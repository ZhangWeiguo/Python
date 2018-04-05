from sklearn import datasets
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

data=datasets.load_digits()
x=data.data
y=data.target
y_names=data.target_names

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3,random_state=33)

cf1=svm.LinearSVC()
cf1.fit(x_train,y_train)
y_test_pre=cf1.predict(x_test)

print cf1.score(x_train,y_train)
print cf1.score(x_test,y_test)


print classification_report(y_test,y_test_pre,target_names=[str(i) for i in y_names])

