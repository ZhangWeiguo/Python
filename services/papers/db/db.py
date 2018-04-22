# -*-encoding:utf8-*-
import web
import time

class DB():
    def __init__(self,user_name, password, database):
        self.db = web.database(dbn = 'mysql',
                               user = user_name,
                               pw = password,
                               db = database)
        self.db_info = {'user':user_name,
                        'pw':password,
                        'db':database}

    def CheckUser(self,id,password):
        r = self.db.select(tables='user_info',
                           what='*',
                           vars={'id': id,'password':password},
                           where='id=$id and password=$password')
        return r


    def AddUser(self,name,password,age,image,description):
        t = int(time.time())
        try:
            n = self.db.insert('user_info',
                           name = name,
                           password = password,
                           age = age,
                           image = image,
                           create_time = t,
                           description = description)
        except:
            return -1
        return n


    def AddPaper(self,user,title,content):
        try:
            n = self.db.insert('paper_info',
                               user = user,
                               title = title,
                               content = content,
                               create_time = int(time.time()))
        except:
            return -1
        return n

    def SelectPaper(self, userId):
        try:
            r = self.db.select(tables = 'paper_info',
                               what = '*',
                               vars = {'user' : userId},
                               where = 'user=$user',
                               order = 'id desc')
        except:
            return -1
        return r

    def SelectAllPaper(self):
        try:
            r = self.db.select(tables = 'paper_info',
                               what = '*',
                               order = 'id desc')
        except:
            return -1
        return r


    def DeletePaper(self, id):
        try:
            self.db.delete('paper_info',
                           vars={'id': id},
                           where='id=$id',)
        except:
            return -1
        return 0