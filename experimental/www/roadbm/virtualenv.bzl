""" WIP on a Bazel rule for portable virtualenv archive. """

VIRTUALENV_SCRIPT = """\
virtualenv --relocatable {env} \
&& echo $(pwd) \
&& source ./{env}/bin/activate \
&& pip install -r {reqs} \
&& tar -czvf {archive} {env}
"""

def _virtualenv_impl(ctx):
  env_name = ctx.label.name
  requirements_file = ctx.file.requirements_file
  archive_out = ctx.outputs.out
  
  print (env_name, requirements_file.path, archive_out.path)
  
  env_dir = ctx.actions.declare_directory(env_name)
  print (env_dir)

  options = dict(
    env=env_name,
    reqs=requirements_file.path,
    archive=archive_out.path
  )

  script = VIRTUALENV_SCRIPT.format(**options)
  print(script)

  ctx.actions.run_shell(
    inputs=[],
    outputs=[env_dir],
    command="virtualenv --relocatable {env}".format(env=env_name)
  )

  # Need to populate of course...

  # And then zip it up.
  ctx.actions.run_shell(
    inputs=[env_dir],
    outputs=[archive_out],
    #progress_message="Getting size of %s" % input.short_path,
    command="tar -czvf {archive} {env}".format(archive=archive_out.path, env=env_dir.path)
  )

virtualenv = rule(
  implementation = _virtualenv_impl,
  attrs = {
    "requirements_file": attr.label(mandatory=True, allow_files=True, single_file=True)
  },
  outputs={
    # "_env_dir" : "%{name}",
    "out": "%{name}.tar.gz",
  }
)






def _temporary_demo_impl(ctx):
  # ctx.actions.declare_file is used for temporary files.
  f = ctx.actions.declare_file(ctx.configuration.bin_dir, "hello")

  #f = ctx.actions.declare_file(ctx.bin_dir, "hello")
  output = ctx.outputs.out

  # As with outputs, each time you declare a file,
  # you need an action to generate it.
  ctx.actions.write(output=f, content=ctx.attr.input_content)

  ctx.actions.run_shell(
    inputs=[f],
    outputs=[output],
    #progress_message="Getting size of %s" % input.short_path,
    command="cat {} > {}".format(f.path, output.path)
  )

  """
  ctx.actions.run(
      inputs=[f],
      outputs=[ctx.outputs.out],
      executable=ctx.executable.binary,
      progress_message="Executing %s" % ctx.executable.binary.short_path,
      arguments=[
          f.path,
          ctx.outputs.out.path,  # Access the output file using
                                 # ctx.outputs.<attribute name>
      ]
  )
  """

temporary_demo = rule(
  implementation=_temporary_demo_impl,
  attrs = {
      # "binary": attr.label(cfg="host", mandatory=True, allow_files=True, executable=True),
      "input_content": attr.string(),
      "out": attr.output(mandatory=True),
  },
)
