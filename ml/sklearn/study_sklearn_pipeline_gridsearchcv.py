from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn import linear_model
from sklearn.grid_search import GridSearchCV
import numpy
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn import pipline
from sklearn.metrics import classification_report as cr
def GridSearchCV_studying():
    data=datasets.load_iris()
    x=data.data
    y=data.target
    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.3)
    cf=linear_model.LogisticRegression()
    C=numpy.linspace(0.5,10,20)
    gsc=GridSearchCV(cf,{'C':C},refit=True,n_jobs=-1)
    gsc.fit(x_train,y_train)


def Pipeline_studyding():
    data=datasets.load_iris()
    x=data.data
    y=data.target
    scaler=StandardScaler()
    cf=linear_model.LogisticRegression()
    pip=pipline.Pipline(steps=[('scale',scaler),('cf',cf)])
    pip.fit(x,y)
    y1=pip.predict(x)
    print cr(y,y1)
    

Pipline_studying()
