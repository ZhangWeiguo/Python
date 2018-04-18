from mysql.connector import pooling

class MysqlClient:
    def __init__(self,config,logger):
        self.pool = pooling.MySQLConnectionPool(pool_name           =   config["pool_name"],
                                                pool_size           =   config["pool_size"],
                                                host                =   config["host"],
                                                port                =   config["port"],
                                                database            =   config["database"],
                                                user                =   config["user"],
                                                password            =   config["password"],
                                                charset             =   "utf8",
                                                pool_reset_session  =   True)

        self.config = config
        self.logger = logger

    def execute(self,sql):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            self.logger("Connect Mysql Failed")
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
            self.logger("Execute Sql Failed:%s"%sql)
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def execute_many(self,sql,data):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            self.logger("Connect Mysql Failed")
        msg = "succ"
        succ = True
        try:
            cursor.executemany(sql,data)
        except Exception as e:
            msg = str(e)
            succ = False
            self.logger("ExecuteMany Sql Failed:%s"%sql)
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def query(self,sql):
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            self.logger("Connect Mysql Failed")
        msg = "succ"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
            self.logger("Query Data Failed:%s"%sql)
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        try:
            result["data"] = cursor.fetchall()
        except Exception as e:
            result["data"] = []
            result["succ"] = False
            result["msg"] = str(e)
        cursor.close()
        conn.close()
        return result