# package(default_visibility = ["//visibility:public"])

load(
    "@pip_grpcio//:requirements.bzl",
    grpcio_requirement = "requirement",
)
load(
    "@pypi_infra//:requirements.bzl",
    infra_requirement = "requirement",
)

py_library(
    name = "calculator_lib",
    srcs = ["calculator.py"],
)

py_binary(
    name = "server",
    srcs = ["server.py"],
    deps = [
        ":calculator_lib",
        "//experimental/grpc_calculator:calculator_pyproto",
        grpcio_requirement("grpcio"),
        infra_requirement("futures"),
    ],
)

py_binary(
    name = "client",
    srcs = ["client.py"],
    deps = [
        "//experimental/grpc_calculator:calculator_pyproto",
        grpcio_requirement("grpcio"),
    ],
)

# TODO(ktreleav): Do Bazel pip installs play well with subpar?
# load("@subpar//:subpar.bzl", "par_binary")
