from bob.commandline.commandline import ExecuteCommandInDirectory

import os

class Compiler:
  def __init__(self, flags, out_dir, src_dir = 'src'):
    self._flags = flags
    self._out_dir = _out_dir
    self._out_existing_files = []

  def _Compiler(self):
    pass

  # Different compilers have differents have different ways of specifying the
  # out directories.
  def _Destination(self, out_dir, raw_compiler):
    pass

  def _Options(self, rule_path, build_rule):
    return []

  def _CompiledObject(self, rule_path, build_rule):
    pass

  # Compilers have different methods of passing in dependencies.
  def _AddDependencies(self, dependencies, raw_compiler):
    pass

  # Many compilers will require a companion object for special options, like
  # C++.
  def Compile(self, rule_path, build_rule, dependencies):
    compiler = self._Compiler()
    self._Destination(self._out_dir, compiler)
    compiler.add_flags(self._flags + build_rule.flags)
    compiler.sources(self._GetSources(rule_path, build_rule))
    self._AddDependencies(dependencies, compiler)
    compiler.options(self._Options(rule_path, build_rule))
    compiler.Execute()
    return self._CompiledObject(rule_path, build_rule)

  def _GetSources(self, dep_name, build_rule):
    rule_path, _ = DecomposeDep(dep_name)
    return [AbsolutePath(rule_path + os.sep + source) for source in build_rule.srcs]

class RawCompiler:
  def __init__(self, compiler_path):
    self._compiler_path = compiler_path
    self._flags = []
    self._options = []
    self._sources = None
    self._deps = []
    self._destination = '.'

  def add_flags(self, flags):
    self._flags.extend(flags)
    return self

  # For some compilers there are special flags which should be treated
  # differently (like g++'s -I).
  def options(self, options):
    return self

  def sources(self, sources):
    self._sources = sources
    return self

  def deps(self, deps):
    self._deps = deps
    return self

  # Different compilers will likely have different ways of specifying a
  # destination.
  def destination(self, destination):
    self._destination = destination
    return self

  def Execute(self):
    if len(self._sources) == 0:
      raise ValueError('Must provide sources to compiler.')
    compiler = ExecuteCommandInDirectory(self._compiler_path)
    compiler.directory(self._destination)
    compiler.flags(self._flags)
    compiler.args(self._sources + self._deps)
    print 'Compiling:\n' + '\n'.join(self._sources)
    compiler.Execute()

def AbsolutePath(local_path):
  return os.path.abspath(local_path)

def DecomposeDep(dep_name):
  [path, rule_name] = dep_name.strip('//').split(':')
  return path, rule_name
