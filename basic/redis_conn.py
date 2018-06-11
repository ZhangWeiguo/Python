# -*- encoding:utf-8 -*-
import redis

class RedisClient(redis.Redis):
    '''
    5 kind data struct: string;hash;list;set;zset
    string:
        set
        get
        change
        delete
    hash:
        set all
        set key value
        get all
        get key value
        delete all
        delete key value
        get keys
    list:
        set all
        insert one
        insert many
        get all
        get part
        get len
        delete one
        delete part
        delete all
    '''
    def __init__(self, host, port=6379, db=0, password=None, **kwargs):
        redis.Redis.__init__(self, host=host, port=port, db=db, password=password, **kwargs)

    def get_string(self, key):
        return self.get(key)
    def set_string(self, key, value, ex=None, px=None, nx=False, xx=False):
        self.set(key, value, ex=ex, px=px, nx=nx, xx=xx)
    def delete_string(self, key):
        self.delete(key)

    def get_many_string(self, keys):
        return self.mget(keys)
    def set_many_string(self, data, ex=None, px=None, nx=False, xx=False):
        self.mset(data, ex=ex, px=px, nx=nx, xx=xx)

    def set_hash(self, name, key, value):
        self.hset(name, key, value)
    def get_hash(self, name, key):
        return self.hget(name, key)
    def delete_hash(self, name, key):
        self.hdel(name, key)

    def set_hash_all(self, name, data):
        if isinstance(data,dict):
            for key in data:
                self.set_hash(name, key, data[key])
        else:
            raise Exception("data should be a dict")
    def get_hash_all(self, name):
        return self.hgetall(name)
    def delete_hash_all(self, name):
        self.delete(self, name)

    def get_hash_keys(self, name):
        return self.hkeys(name)


    def set_list(self, name, index, value):
        self.lset(name, index, value)
    def get_list(self, name, index):
        return self.lindex(name, index)
    def insert_list(self, name, where, refvalue, value):
        self.linsert(name, where, refvalue, value)

    def pop_list(self, name, kind="fist"):
        if kind in ["first","last"]:
            if kind == "first":
                return self.lpop(name)
            else:
                return self.rpop(name)
        else:
            raise Exception("kind should be first or lasst")

    def push_list(self, name, value, kind="fist"):
        if kind in ["first","last"]:
            if kind == "first":
                return self.lpush(name, value)
            else:
                return self.lpushx(name, value)
        else:
            raise Exception("kind should be first or lasst")

    def trim_list(self, name, value, num=0):
        self.lrem(name, value, num)
        self.ltrim()


    def set_list_all(self, name, data):
        if isinstance(data, list):
            for i in range(len(data)):
                self.lset(name, i, data[i])
        else:
            raise Exception("data should be list")
    def get_list_all(self, name):
        return self.lrange(name, start=0, end=self.llen(name))
    def get_list_part(self, name, start, end):
        return self.lrange(name, start=start, end=end)
    def get_list_len(self, name):
        return self.llen(name)






if __name__ == "__main__":
    r = RedisClient(host="127.0.0.1", port=6379, db=1, password="foobared")

    # r.set_string(key="name", value="zhangweiguo", ex=6)
    # print r.get_string("name")
    # r.delete_string("name")
    # print r.get_string("name")

    # r.set_many_string({"name1":"zhangone","name2":"zhangtwo"})
    # print r.get_many_string(["name1","name2"])


    # r.set_hash("master","name","zhangweiguo")
    # r.set_hash("master","age",14)
    # print r.get_hash("master","age")

    # r.delete_hash("master","name")
    # print r.get_hash("master", "age")
    # print r.get_hash("master", "name")

    # r.delete("master")
    # print r.get_hash("master","age")

    # r.set_hash_all("master",{"name":"zhangsan","age":14})
    # print r.get_hash_all("master")
    # r.delete_hash_all("master")
    # print r.get_hash("master", "name")
    # print r.get_hash_all("master")



    # c = r.connection_pool.make_connection()
    # c.send_command("set name zhangsan")
    # c.send_command("get name zhangsan")


