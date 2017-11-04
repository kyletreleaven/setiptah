load(":virtualenv.bzl", "virtualenv", "temporary_demo")

virtualenv(
  name = "roadbm_env",
  requirements_file="requirements.txt"
)


CONTENT = """\
Hello, World!
"""

temporary_demo(
  name = "temp_demo",
  input_content=CONTENT,
  out="temp.txt",
)