

git_repository(
	name = "subpar",
	remote = "https://github.com/google/subpar",
	# Why isn't HEAD supported!?
	commit = "74529f1df2178f07d34c72b3d270355dab2a10fc"
)

# Figure out how to get protobuf libraries compiling!
git_repository(
	name = "protobuf",
	remote = "https://github.com/google/protobuf",
	commit = "HEAD"
)

# Enable proto rules in the workspace.
git_repository(
  name = "org_pubref_rules_protobuf",
  remote = "https://github.com/pubref/rules_protobuf",
  tag = "v0.8.0",
  #commit = "..." # alternatively, use latest commit on master
)

# Enable language proto rules in the workspace.
load("@org_pubref_rules_protobuf//java:rules.bzl", "java_proto_repositories")
java_proto_repositories()

load("@org_pubref_rules_protobuf//cpp:rules.bzl", "cpp_proto_repositories")
cpp_proto_repositories()

load("@org_pubref_rules_protobuf//python:rules.bzl", "py_proto_repositories")
py_proto_repositories()

# Enable Scala rules in the workspace.
rules_scala_version="031e73c02e0d8bfcd06c6e4086cdfc7f3a3061a8" # update this as needed

http_archive(
             name = "io_bazel_rules_scala",
             url = "https://github.com/bazelbuild/rules_scala/archive/%s.zip"%rules_scala_version,
             type = "zip",
             strip_prefix= "rules_scala-%s" % rules_scala_version
             )

load("@io_bazel_rules_scala//scala:scala.bzl", "scala_repositories")
scala_repositories()
