import grpc

# import the generated classes
from experimental.grpc_calculator import calculator_pb2
from experimental.grpc_calculator import calculator_pb2_grpc

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = calculator_pb2_grpc.CalculatorStub(channel)


import sys
n = float(sys.argv[1])

# create a valid request message
number = calculator_pb2.Number(value=n)

# make the call
response = stub.SquareRoot(number)

# et voila
print(response.value)
