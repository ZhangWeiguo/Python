# -*-encoding:utf-8-*-
from svd import SVD
import numpy,json

def test(filename = "action_train.log"):
    Model = SVD(20)
    Model.restore('user_vector','video_vector')

    f = file(filename,'r')
    all_data = f.read().split("\n")
    order = range(len(all_data))
    f.close()

    E = {}
    N = len(all_data)
    n = {}
    print "All %d samples"%N
    for s in all_data:
        L = s.split(",")
        if len(L) == 3:
            user_id = L[0]
            video_id = L[1]
            action = L[2].replace("\n", "")
            score = Model.predict(user_id, video_id)
            if score != -1:
                value = score
                if action in E:
                    E[action] += value
                    n[action] += 1
                else:
                    E[action] = value
                    n[action] = 1
    for i in E:
        print "%15s: samples: %10d(%1.4f), value: %7f"%(i,n[i],float(n[i])/N,E[i]/n[i])


test(filename = "action_train.log")
test(filename = "action_test.log")

