# -*- encoding:utf-8 -*-

import grpc
import time
import userid_pb2_grpc
import userid_pb2
from userid_pb2_grpc import UserServicer
from userinfo_pb2 import UserInfo
from concurrent import futures



HOST = 'localhost'
PORT = '8080'


class EasyService(UserServicer):
    def GetUserInfo(self, request, context):
        u = UserInfo()
        u.id = request.id
        u.name = "zhangtest"
        print("Get User Id: %d"%(request.id))
        return u


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    userid_pb2_grpc.add_UserServicer_to_server(EasyService(), server)
    server.add_insecure_port('%s:%s'%(HOST,PORT))
    server.start()
    try:
        while True:
            time.sleep(5)
            print("No Request!")
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()