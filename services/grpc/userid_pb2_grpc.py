# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import userid_pb2 as userid__pb2
import userinfo_pb2 as userinfo__pb2


class UserStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetUserInfo = channel.unary_unary(
        '/grpc.User/GetUserInfo',
        request_serializer=userid__pb2.UserId.SerializeToString,
        response_deserializer=userinfo__pb2.UserInfo.FromString,
        )


class UserServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetUserInfo(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetUserInfo': grpc.unary_unary_rpc_method_handler(
          servicer.GetUserInfo,
          request_deserializer=userid__pb2.UserId.FromString,
          response_serializer=userinfo__pb2.UserInfo.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'grpc.User', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
