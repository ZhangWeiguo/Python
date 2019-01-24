# -*- encoding: utf-8 -*-
import grpc
import os
import sys
from userid_pb2_grpc import UserStub
from userid_pb2 import UserId

HOST = 'localhost'
PORT = '8080'


def grpc_request():
    conn = grpc.insecure_channel("%s:%s"%(HOST,PORT))
    client = UserStub(channel = conn)
    u = UserId(id=12)
    response = client.GetUserInfo(u)
    print(str(response))
    # print(response.SerializeToString())
    # print(u.ParseFromString(s))


if __name__ == '__main__':
    grpc_request()
