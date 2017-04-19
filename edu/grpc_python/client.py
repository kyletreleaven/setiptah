import grpc

import gen.hello_pb2 as hello_pb2
import gen.hello_pb2_grpc as hello_pb2_grpc


def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = hello_pb2_grpc.GreeterStub(channel)
  response = stub.SayHello(hello_pb2.HelloRequest(name='you'))
  print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()