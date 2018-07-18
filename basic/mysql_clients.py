from mysql.connector import pooling

class MysqlClient:
    def __init__(self,**kwargs):
        self.pool = pooling.MySQLConnectionPool(pool_name           =   kwargs["pool_name"],
                                                pool_size           =   kwargs["pool_size"],
                                                host                =   kwargs["host"],
                                                port                =   kwargs["port"],
                                                database            =   kwargs["database"],
                                                user                =   kwargs["user"],
                                                password            =   kwargs["password"],
                                                charset             =   "utf8",
                                                pool_reset_session  =   True)

        self.config = kwargs

    def execute(self,sql):
        msg = "succ"
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            msg = "Connect Failed"
        succ = True
        try:
            cursor.execute(sql)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def execute_many(self,sql,data):
        msg = "succ"
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            msg = "Connect Failed"
        succ = True
        try:
            cursor.executemany(sql,data)
        except Exception as e:
            msg = str(e)
            succ = False
        result = {}
        result["msg"] = msg
        result["succ"] = succ
        conn.commit()
        cursor.close()
        conn.close()
        return result

    def query(self,sql):
        msg = "succ"
        try:
            conn = self.pool.get_connection()
            cursor = conn.cursor(dictionary = True)
        except:
            msg = "Connect Failed"
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
        cursor.close()
        conn.close()
        return result