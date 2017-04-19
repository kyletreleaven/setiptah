Bare minimum Python code from grpc.

http://www.grpc.io/docs/quickstart/python.html

git clone https://github.com/grpc/grpc

python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/helloworld.proto

