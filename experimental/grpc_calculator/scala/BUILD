load("@io_bazel_rules_scala//scala:scala.bzl", "scala_binary", "scala_repl")

scala_binary(
    name = "calculator_client",
    srcs = [
        "CalculatorClient.scala",
    ],
    main_class = "org.setiptah.experimental.grpc_calculator.scala.CalculatorClient",
    deps = [
        "//experimental/grpc_calculator:calculator_java_proto",
    ],
)

scala_repl(
    name = "calculator_repl",
    deps = [
        "//experimental/grpc_calculator:calculator_java_proto",
    ],
)
