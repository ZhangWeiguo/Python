# -*- encoding:utf-8 -*-
import redis

# pool = redis.ConnectionPool(host='127.0.0.1', port=6379, password="foobared", db=0, decode_responses=True)
# r = pool.make_connection()
# r = redis.Redis(connection_pool=pool)

# # r.set('food', 'beef', px=3)
# print(r.get('name'))


class RedisClient:
    def __init__(self,host, port=6379,decode_responses=True):
        pass
    
    def get(self):
        pass
    def set(self):
        pass

