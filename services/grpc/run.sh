py -2 -m pip install grpcio
py -2 -m pip install grpcio-tools


# D:\\protobuf\\bin\\protoc.exe --python_out=./ userinfo.proto
# D:\\protobuf\\bin\\protoc.exe --python_out=./ userid.proto

py -2 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./userinfo.proto
py -2 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./userid.proto
