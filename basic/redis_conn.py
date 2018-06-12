# -*- encoding:utf-8 -*-
import redis

class RedisClient(redis.Redis):
    '''
    5 kind data struct: string;hash;list;set;zset
    getAll/setAll
    '''
    def __init__(self, host, port=6379, db=0, password=None, **kwargs):
        redis.Redis.__init__(self, host=host, port=port, db=db, password=password, **kwargs)

    def get_string(self, key):
        return self.get(key)
    def set_string(self, key, value, ex=None, px=None, nx=False, xx=False):
        self.set(key, value, ex=ex, px=px, nx=nx, xx=xx)

    def set_hash_all(self, name, data):
        if isinstance(data, dict):
            for key in data:
                self.hset(name, key, data[key])
        else:
            raise Exception("data should be a dict")
    def get_hash_all(self, name):
        return self.hgetall(name)


    def set_list_all(self, name, data):
        if isinstance(data, list):
            data.reverse()
            self.delete(name)
            self.lpush(name, *data)
        else:
            raise Exception("data should be list")
    def get_list_all(self, name):
        return self.lrange(name, start=0, end=self.llen(name))

    def set_set_all(self, name, data):
        if isinstance(data, set):
            self.delete(name)
            self.sadd(name, *data)
        else:
            raise Exception("data should be set")

    def get_set_all(self, name):
        return self.sscan(name)


    def set_zset_all(self, name, data):
        if isinstance(data, dict):
            self.delete(name)
            self.zadd(name, **data)
        else:
            raise Exception("data should be dict")

    def get_zset_all(self, name):
        return self.zscan(name)


if __name__ == "__main__":
    r = RedisClient(host="127.0.0.1", port=6379, db=1, password="foobared")

    r.set("name","zhangsan",ex=10)
    r.set("age",14,ex=10)
    print r.get("name")
    print r.get("age")
    r.incr("age",4)
    print r.get("age")

    r.hset("master","name","zhangsan")
    r.hset("master","age","17")
    r.hset("master","country","CN")
    print r.hgetall("master")

    r.set_list_all("videos",range(10))
    print r.get_list_all("videos")

    r.set_set_all("videos",set(range(10)))
    print r.get_set_all("videos")

    r.set_zset_all("videos",{"1":12,"2":34,"4":56})
    print r.get_zset_all("videos")





