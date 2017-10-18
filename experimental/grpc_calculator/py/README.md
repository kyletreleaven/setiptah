Following along with: https://engineering.semantics3.com/a-simplified-guide-to-grpc-in-python-6c4e25f0c506 ;

however, with bazel grpc tooling integration:

https://github.com/pubref/rules_protobuf
https://grpc.io/blog/bazel_rules_protobuf

Found an example
https://github.com/pubref/rules_protobuf/tree/master/examples/helloworld/python
mentioned in bazel group discussion
https://groups.google.com/forum/#!topic/bazel-discuss/P63WUMb4a80

Another related demo.
https://github.com/korfuri/grpc-bazel

# Who are these people?
pubref.org
https://github.com/pubref

Try a simpler demo?
https://grpc.io/docs/tutorials/basic/python.html

```
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. calculator.proto
```
