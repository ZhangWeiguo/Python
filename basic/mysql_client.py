from mysql.connector import connection

class MysqlClient:
    def __init__(self,config):
        self.config = config
        self.conn = connection.MySQLConnection(user      =   config["user"], 
                                               password  =   config["password"],
                                               host      =   config["host"],
                                               port      =   config["port"],
                                               database  =   config["database"],
                                               charset   =   "utf8")
        self.cursor = self.conn.cursor(dictionary = True)

    def execute(self,sql):
        cursor = self.cursor
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        self.conn.commit()
        return result

    def execute_many(self,sql,data):
        cursor = self.cursor
        msg = "succ"
        succ = True
        try:
            cursor.executemany(sql,data)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        self.conn.commit()
        return result

    def query(self,sql):
        cursor = self.cursor
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        try:
            result["data"] = cursor.fetchall()
        except Exception as e:
            result["data"] = []
            result["succ"] = False
            result["msg"] = str(e)
        return result
    
    def close(self):
        result = {}
        try:
            self.cursor.close()
            self.conn.close()
            result["succ"] = True
            result["msg"] = ""
        except Exception as e:
            result["succ"] = False
            result["msg"] = str(e)
        return result
