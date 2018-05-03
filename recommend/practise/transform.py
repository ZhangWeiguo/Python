# -*-encoding:utf-8-*-
import numpy,os
from conf import action as main_action

def concat_file(filenames = [], filename = "action_train.log"):
    if os.path.exists(filename):
        os.remove(filename)
    Data = {}
    action_list = main_action
    for i in filenames:
        f = file(i,'r')
        while True:
            s = f.readline()
            if not s:
                break
            L = s.split(",")
            if len(L) == 3:
                user_id = L[0]
                video_id = L[1]
                action = L[2].replace("\n","")
                if len(user_id)>=10 and len(video_id)>=10:
                    if user_id in Data:
                        if video_id in Data[user_id]:
                            if action_list.index(action) > action_list.index(Data[user_id][video_id]):
                                Data[user_id][video_id] = action
                        else:
                            Data[user_id][video_id] = action
                    else:
                        Data[user_id] = {}
                        Data[user_id][video_id] = action
        f.close()
        print "finished processing %s"%i
    f = file(filename, 'w')
    for user in Data:
        for video in Data[user]:
            try:
                f.write("%s,%s,%s\n"%(user,video,Data[user][video]))
            except:
                print user,video,Data[user][video]
    f.close()


if __name__ == "__main__":
    # L = []
    # path = "data\\"
    # filename = "action_train.log"
    # if os.path.exists(filename):
    #     os.remove(filename)
    # for i in os.listdir("data"):
    #     if (i.endswith("log") and "action1204" in i):
    #         L.append(path+i)
    # print L
    # concat_file(L,filename)

    L = []
    path = "data\\"
    filename = "action_test.log"
    if os.path.exists(filename):
        os.remove(filename)
    for i in os.listdir("data"):
        if (i.endswith("log") and "action1205" in i):
            L.append(path + i)
    print L
    concat_file(L, filename)




