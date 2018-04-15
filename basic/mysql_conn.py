# -*- coding: utf-8 -*-
'''
created by zwg in 2018-03-08
'''


import MySQLdb
import MySQLdb.cursors

class MysqlClient:
    def __init__(self,config,logger):
        self.logger = logger
        self.conn = None
        self.cursor = None
        try:
            self.conn = MySQLdb.connect(
                host        =   config["host"],
                port        =   config["port"],
                user        =   config["user"],
                passwd      =   config["passwd"],
                db          =   config["db"],
                use_unicode =   True,
                charset     =   'UTF8',
                cursorclass =   MySQLdb.cursors.DictCursor
            )
            self.cursor = self.conn.cursor()
        except Exception,e:
            self.logger("Connect Mysql Failed: "+ str(e))

    def query_fetchall(self,sql):
        data = None
        try:
            self.cursor.execute(sql)
        except Exception,e:
            self.logger("Mysql Execute Failed: "+ str(e))
        try:
            data = self.cursor.fetchall()
        except Exception,e:
            self.logger("Get Data Failed: " + str(e))
        return data

    def execute(self,sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception,e:
            print e,sql
            self.logger("Mysql Execute Failed: " + str(e))

    def execute_many(self,sql,parm):
        try:
            self.cursor.executemany(sql,parm)
            self.conn.commit()
        except Exception,e:
            self.logger("Mysql Executemany Failed: "+ str(e))

'''
mysqlConfig = {
    'name'   : 'ugc_video_consume',
    'host'   : '127.0.0.1',
    'port'   : 55556,
    'user'   : 'main_wapka_mobi',
    'passwd' : 'JKjk^%$lddada',
    'db'     : 'ugc_online'
}
'''