# -*- encoding:utf-8 -*-
import numpy,gc,time,os
from model import Model
'''
> RecallModel有两个模型：model和model_backup
> model           用于线上模型，只读
> model_backup    用于备份，只写


初始化
    * model从前3天数据中训练
    * model计算距离矩阵
    * model文件保存模型和向量


热更新(每三小时更新一次)
    * model_backup从前3天数据中训练
    * model_backup计算距离矩阵
    * model_backup文件保存模型和向量

    * model=model_backup
    * model文件保存模型和向量

重启
    * model恢复
        ** model从model自己的文件恢复向量
        ** model从model自己的模型恢复向量
        ** model从model_bcakup的文件恢复向量
        ** model从model_backup的模型恢复向量

    * model计算距离矩阵
    * model文件保存向量
    * model_backup文件保存向量


train_files = ["user_action.2018042801.log","user_action.2018042802.log"]

Model需要实现的API

class Model:
    def __init__(self)
        pass
    def train(self, train_files):
        pass
    def save_vecs(self):
        pass
    def recover_from_vec(self):
        pass
    def recover_from_model(self):
        pass
    def recall(self,item_id, max_num):
        pass
    def __save(self,data,filename):
        pass
    def __cal_items_dist(self):
        pass
    def copy(self,model):
        pass
    def predict(self, **kwargs):
        pass
    def error(self, **kwargs):
        pass
'''


class RecallModel:
    def __init__(self,
                train_files                 = [],
                model_path                  = "data/model", 
                items_path                  = "data/items.vec",
                users_path                  = "data/users.vec",
                items_dict_path             = "data/items.dict",
                users_dict_path             = "data/users.dict",
                model_backup_path           = "data/model_backup", 
                items_backup_path           = "data/items_backup.vec",
                users_backup_path           = "data/users_backup.vec",
                items_backup_dict_path      = "data/items_backup.dict",
                users_backup_dict_path      = "data/users_backup.dict"):
        self.model_path                 = model_path
        self.items_path                 = items_path
        self.users_path                 = users_path
        self.users_dict_path            = users_dict_path
        self.items_dict_path            = items_dict_path
        self.model_backup_path          = model_backup_path
        self.items_backup_path          = items_backup_path
        self.users_backup_path          = users_backup_path
        self.users_backup_dict_path     = users_backup_dict_path
        self.items_backup_dict_path     = items_backup_dict_path

        self.model              = Model(model_path      = self.model_path, 
                                        items_path      = self.items_path,
                                        users_path      = self.users_path,
                                        items_dict_path = self.items_dict_path,
                                        users_dict_path = self.users_dict_path)
        self.model_backup       = Model(model_path      = self.model_backup_path, 
                                        items_path      = self.items_backup_path,
                                        users_path      = self.users_backup_path,
                                        users_dict_path = self.users_backup_dict_path,
                                        items_dict_path = self.items_backup_dict_path)

        self.model.recover_from_vec()
        try:
            self.model.recover_from_vec()
        except:
            print("Model Init From Vec Failed!")
            try:
                self.model.recover_from_model()
            except:
                print("Model Init From Model Failed!")
                try:
                    self.model_backup.recover_from_vec()
                except:
                    print("ModelBackup Init From Vec Failed!")
                    try:
                        self.model_backup.recover_from_model()
                    except:
                        print("ModelBackup Init From Model Failed!")
                        self.model.train(train_files)
                        

        
        if self.model and not self.model_backup:
            self.model_backup.copy(self.model)
            self.model_backup.save_vecs()
        elif not self.model and self.model_backup:
            self.model.copy(self.model_backup)
            self.model.save_vecs()
        

    def update_model(self,train_files,**kwargs):
        self.model_backup.train(train_files,**kwargs)
        self.model_backup.save_vecs()
        self.model.copy(self.model_backup)
        self.model.save_vecs()

    def recall(self, item_id, max_num):
        ids = []
        try:
            ids = self.model.recall(item_id, max_num)
        except:
            print("Recall From Model Failed!")
            try:
                ids = self.model_backup.recall(item_id, max_num)
            except:
                print("Recall From BackupModel Failed!")
        return ids

    def get_ctime(self):
        return self.model.create_time
    def __get_item_vec(self, item_id):
        return self.model.items[item_id]["vec"]
    def __get_user_vec(self, user_id):
        return self.model.users[user_id]["vec"]




