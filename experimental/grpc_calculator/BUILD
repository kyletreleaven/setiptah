package(default_visibility = ["//visibility:public"])

load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_library")
load("@org_pubref_rules_protobuf//java:rules.bzl", "java_proto_library")

py_proto_library(
    name = "calculator_pyproto",
    protos = [
        "calculator.proto",
    ],
    # proto_deps = ["//examples/proto:py",],
    verbose = 1,  # 0=no output, 1=show protoc command, 2+ more...
    with_grpc = True,
)

java_proto_library(
    name = "calculator_java_proto",
    protos = [
        "calculator.proto",
    ],
    # proto_deps = ["//examples/proto:py",],
    verbose = 1,  # 0=no output, 1=show protoc command, 2+ more...
    with_grpc = True,
)
