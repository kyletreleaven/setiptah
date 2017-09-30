load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_library")

"""
py_proto_library(
    name = "py",
    proto_deps = [
        "//examples/proto:py",
    ],
    protos = [
        ":protos",
    ],
    with_grpc = True,
)
"""

py_proto_library(
  name = "calculator_pyproto",
  protos = [
    "calculator.proto",
  ],
  with_grpc = True,
  verbose = 1,  # 0=no output, 1=show protoc command, 2+ more...
)

load("@subpar//:subpar.bzl", "par_binary")

py_library(
  name = "calculator_lib",
  srcs = ["calculator.py"],
)

par_binary(
  name = "server",
  srcs = ["server.py",],
  deps = [
    ":calculator_pyproto",
    ":calculator_lib",
  ],
)
