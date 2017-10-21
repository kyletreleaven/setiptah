# ================================================================
# Enable Scala rules in the workspace
# ================================================================
rules_scala_version="1a856c279afff55dd1a7f10ba99c75a7fa9a3a0a"

http_archive(
             name = "io_bazel_rules_scala",
             url = "https://github.com/bazelbuild/rules_scala/archive/%s.zip"%rules_scala_version,
             type = "zip",
             strip_prefix= "rules_scala-%s" % rules_scala_version
             )

load("@io_bazel_rules_scala//scala:scala.bzl", "scala_repositories")
scala_repositories()

# ================================================================
# Language specific proto rules
# ================================================================

# Enable proto rules in the workspace.
git_repository(
  name = "org_pubref_rules_protobuf",
  remote = "https://github.com/pubref/rules_protobuf",
  tag = "v0.8.1",
  #commit = "..." # alternatively, use latest commit on master
)

# Enable language proto rules in the workspace.
load("@org_pubref_rules_protobuf//java:rules.bzl", "java_proto_repositories")
java_proto_repositories()

load("@org_pubref_rules_protobuf//cpp:rules.bzl", "cpp_proto_repositories")
cpp_proto_repositories()

load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_repositories")
py_proto_repositories()

# ================================================================
# io_bazel_rules_python support for pip_import
# ================================================================

"""Python rules with pip_import support"""
git_repository(
    name = "io_bazel_rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "44fdf5f24a4b634ef7b0f86e7a017f4d8d5aa899",
)

"""
# Obtain io_bazel_rules_python by github_archive
load("@org_pubref_rules_protobuf//protobuf:rules.bzl", "github_archive")

github_archive(
    name = "io_bazel_rules_python",
    commit = "fa77c9c1118380e066c88b955c90fb3c7353429e",
    org = "bazelbuild",
    repo = "rules_python",
    sha256 = "7d06126d0d10ea8e63cc7eaf774d9ecebcd9583094ee8e93b0035da659eab5c1",
)
"""

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

# ================================================================
# pip_import for infrastructural packages from PyPI
# ================================================================

pip_import(
    name = "pypi_infra",
    requirements = "//tools/pypi_infra:requirements.txt",
)

load("@pypi_infra//:requirements.bzl", infra_pip_install="pip_install")
infra_pip_install()

# ================================================================
# pip_import for grpc support
# ================================================================

pip_import(
  name = "pip_grpcio",
  requirements = "@org_pubref_rules_protobuf//python:requirements.txt",
)

load("@pip_grpcio//:requirements.bzl", pip_grpcio_install = "pip_install")
pip_grpcio_install()


# ================================================================
# Python additional support
# ================================================================

# TODO(ktreleav): Is there a "resources" library to complement subpar?

git_repository(
  name = "subpar",
  remote = "https://github.com/google/subpar",
  # Why isn't HEAD supported!?
  commit = "74529f1df2178f07d34c72b3d270355dab2a10fc"
)
