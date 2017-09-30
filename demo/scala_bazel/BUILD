load("@io_bazel_rules_scala//scala:scala.bzl", "scala_library", "scala_binary", "scala_test")

# TODO(ktreleav): Need to fix this target; currently failing on:
"""
The `set` constructor for depsets is deprecated and will be removed. Please use the `depset` constructor instead.
You can temporarily enable the deprecated `set` constructor by passing the flag --incompatible_disallow_set_constructor=false
"""
scala_binary(
  name = "hello_scala",
  srcs = ["Main.scala"],
  main_class = "Main",
)

"""
load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_compile")

py_proto_compile(
  name = "message_proto",
  protos = ["myproto.proto"],
  with_grpc = True, # only one file is generated with or without grpc
)
"""

"""
load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_library")

py_proto_library(
  name = "myproto_py",
  protos = ["myproto.proto"],
  # with_grpc = True,
)
"""

py_binary(
  name = "quick",
  srcs = [
    "quick_py.py",
  ],
  main = "quick_py.py",
  deps = [
    # ":myproto_py",
  ],
)
