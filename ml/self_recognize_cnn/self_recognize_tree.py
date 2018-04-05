# -*-encoding:utf-8 -*-
'''
created by zwg in 2017-09-23
'''
# 识别自拍头像图片(集成方法)

import os,numpy,shelve,random
from sklearn import svm,tree,ensemble,linear_model,neural_network
from sklearn.cross_validation import train_test_split
from matplotlib import pyplot
from sklearn.externals import joblib
from self_data_pre import shape,Sex_file,image2array
from PIL import Image

Model_file = 'SelfRecognize_Tree'
Test_dir = "..\\data\\sex\\image\\all_jpg"




def train():
    Data = shelve.open(Sex_file)
    data = Data['Data']
    target = Data['Target']
    Data.close()
    train_data,test_data,train_target,test_target = \
        train_test_split(data,
                         target,
                         test_size= 0.2,
                         random_state=33)
    print ("begin to train")
    L = neural_network.MLPClassifier(hidden_layer_sizes=(1024, 128,),activation="logistic",max_iter=2000)
    # L = svm.LinearSVC(C=3.0, max_iter=2000)
    # L = linear_model.SGDClassifier(n_jobs=-1,eta0=0.05,alpha = 0.1,max_iter=2000)
    # L = ensemble.RandomForestClassifier(n_estimators=400,max_depth=200,n_jobs = -1)
    # L = ensemble.ExtraTreesClassifier(n_jobs=-1,n_estimators=200,max_depth=10)
    # L = gaussian_process.GaussianProcessClassifier()
    # L = ensemble.BaggingClassifier(base_estimator=svm.LinearSVC,n_estimators=20,n_jobs=-1)
    L.fit(train_data, train_target)
    print ("end to train")
    print (L.score(train_data, train_target))
    print (L.score(test_data, test_target))
    joblib.dump(L, Model_file)


def test():
    L = joblib.load(Model_file)
    All_videos = os.listdir(Test_dir)
    N = len(All_videos)
    for i in range(15):
        filename = All_videos[i]
        path = os.path.join(Test_dir, filename)
        data = image2array(path, shape=shape).reshape(1, -1)
        pyplot.figure(i)
        pyplot.imshow(numpy.array(Image.open(path)))
        pyplot.title(str(L.predict(data)[0]))
    pyplot.show()

# save_data()
train()
# test()