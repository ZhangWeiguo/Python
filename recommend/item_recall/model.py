# -*-encoding:utf-8 -*-
# created by wegozng in 20180430

import tensorflow as tf
import numpy,os,json,math,time
from model_svd import train,recover

'''
训练后保存模型和向量
恢复可以从模型恢复或者从向量文件直接恢复
embeding的ID是数字ID
items       = {1: [vec] }
items_dict  = {1: "video_id"}
items_vdict = {"video_id": 1}
'''

class Model:
    def __init__(self,
                    model_path      = "data/model", 
                    items_path      = "data/items.vec",
                    users_path      = "data/users.vec",
                    items_dict_path = "data/items.dict",
                    users_dict_path = "data/users.dict" ):
        self.items              = {}
        self.users              = {}
        self.items_dist         = {}
        self.items_dict         = {}
        self.users_dict         = {}
        self.items_vdict        = {}
        self.users_vdict        = {}
        self.model_path         = model_path
        self.items_path         = items_path
        self.users_path         = users_path
        self.items_dict_path    = items_dict_path
        self.users_dict_path    = users_dict_path
        self.create_time        = "unknow"

    def train(self,     
            train_files             = [],
            item_dim                = 50,
            user_dim                = 50,
            other_dim               = 0,
            goal_dim                = 1,
            batch_size              = 2000,
            train_epochs            = 3,
            learning_rate           = 0.0001,
            learning_rate_decay     = 0.5,
            decay_steps             = 5000,
            input_regular_rate      = 0.00001):
        # custom model to train
        # save the mode and input items vec && users vec
        users_path      = self.users_path
        items_path      = self.items_path
        items_dict_path = self.items_dict_path
        users_dict_path = self.users_dict_path
        config = {
                "train_files"           : train_files,
                "model_path"            : self.model_path,
                "item_dim"              : item_dim,
                "user_dim"              : user_dim,
                "other_dim"             : other_dim,
                "goal_dim"              : goal_dim,
                "batch_size"            : batch_size,
                "train_epochs"          : train_epochs,
                "learning_rate"         : learning_rate,
                "learning_rate_decay"   : learning_rate_decay,
                "decay_steps"           : decay_steps,
                "input_regular_rate"    : input_regular_rate
        }
        self.items,self.users,self.items_vdict,self.users_vdict = train(**config)
        self.users_dict = self.__reverse_dict(self.users_vdict)
        self.items_dict = self.__reverse_dict(self.items_vdict)
        t = [os.path.getctime(i) for i in train_files]
        self.create_time = time.strftime("%Y%m%d%H",time.localtime(max(t)))
        # self.__cal_items_dist()

    def save_vecs(self):
        self.__save(self.items, self.items_path)
        self.__save(self.users, self.users_path)
        self.__save(self.users_dict,self.users_dict_path)
        self.__save(self.items_dict,self.items_dict_path)
    
    def recover_from_vec(self):
        self.items          = self.__recover(self.items_path)
        self.users          = self.__recover(self.users_path)
        self.items_dict     = self.__recover(self.items_dict_path)
        self.users_dict     = self.__recover(self.users_dict_path)
        self.items_vdict    = self.__reverse_dict(self.items_dict)
        self.users_vdict    = self.__reverse_dict(self.users_dict)
        self.__cal_items_dist()

    def recover_from_model(self):
        self.items_dict     = self.__recover(self.items_dict_path)
        self.users_dict     = self.__recover(self.users_dict_path)
        self.items_vdict    = self.__reverse_dict(self.items_dict)
        self.users_vdict    = self.__reverse_dict(self.users_dict)
        self.items,self.users = recover(model_path  = self.model_path,
                                        user_num    = len(self.users_dict),
                                        item_num    = len(self.items_dict))
        self.__cal_items_dist()


    def recall(self,item_id, max_num):
        ids = []
        try:
            index_id = self.items_vdict[video_id]
            item_dist = self.items_dist[index_id]
            if len(item_dist) < max_nums:
                ids = item_dist
            else:
                ids = item_dist[0:max_num]
        except:
            pass
        return ids

    def __save(self,data,filename):
        f = open(filename,'w')
        data = [ json.dumps(
                {"id"       :key,
                "value"     :data[key]}) + "\n" for key in data]
        f.writelines(data)
        f.close()
    def __recover(self,filename):
        f = open(filename,'r')
        data = f.read()
        data = data.split("\n")
        if len(data) <= 10:
            raise Exception("FileSize Is Too Small")
        data = [json.loads(i) for i in data]
        dict_data = {}
        for unit in data:
            dict_data[unit["id"]] = unit["value"]
        return dict_data

    def __cal_items_dist(self):
        self.items_dist = {}
        for itemi in self.items:
            Li = self.items[itemi]
            item_dist = [(itemj,self.__dist(Li,self.items[itemj])) for itemj in self.items]
            item_dist = sorted(item_dist, key= lambda L:L[1], reverse=True)
            self.items_dist[i] = item_dist

    
    def __dist(self,L1,L2):
        d1 = math.sqrt(sum([i**2 for i in L1]))
        d2 = math.sqrt(sum([i**2 for i in L2]))
        d0 = sum([L1[i]*L2[i] for i in range(len(L1))])
        return d0/(d1*d2 + 1e-30)
    def __reverse_dict(self,data):
        new = {}
        for i in data:
            new[data[i]] = i
        return new

    def copy(self,model):
        self.items          = model.items
        self.users          = model.users
        self.users_dict     = model.users_dict
        self.items_dict     = model.items_dict
        self.users_vdict    = model.users_vdict
        self.items_vdict    = model.items_vdict
        self.items_dist     = model.items_dist
        self.create_time    = model.create_time

    def predict(self, **kwargs):
        raise Exception("UnComplete Methods")
    def error(self, **kwargs):
        raise Exception("UnComplete Methods")


if __name__ == "__main__":
    train_files = [ "data/user_action.2018042815.log",
                    "data/user_action.2018042814.log",
                    "data/user_action.2018042813.log",
                    "data/user_action.2018042812.log",
                    "data/user_action.2018042811.log",
                    "data/user_action.2018042810.log"]
    train_files = [ "data/user_action.2018042806.log"]
    M = Model()
    M.train(train_files)
    M.save_vecs()