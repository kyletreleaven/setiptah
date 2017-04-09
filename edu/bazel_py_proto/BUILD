
proto_library(
	name = "string_message",
	srcs = ["string_message.proto"],
)

load("@subpar//:subpar.bzl", "par_binary")

par_binary(
	name = "main",
	srcs = ["main.py",],
	deps = [
		":lib1",
	],
)

py_library(
	name = "lib1",
	srcs = ["lib1.py"],
	deps = [
		":lib2",
	],
)

py_library(
	name = "lib2",
	srcs = ["lib2.py"],
)

