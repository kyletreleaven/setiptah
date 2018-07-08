load("@io_bazel_rules_jsonnet//jsonnet:jsonnet.bzl",
  "jsonnet_to_json",
  "jsonnet_library")

jsonnet_library(
    name = "jsonnet_lib",
    srcs = ["lib.libsonnet"],
)

jsonnet_to_json(
    name = "some_json",
    src = "src.jsonnet",
    outs = ["some.json"],
    deps = [":jsonnet_lib"],
    ext_strs = {
      "x": "some-stuff!"
    }
)