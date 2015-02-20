from bob.commandline.commandline import ExecuteCommandInDirectory

class Compiler:
  def __init__(self, flags, out_dir):
    self._flags = flags
    self._out_dir = _out_dir

  def _Compiler(self):
    pass

  # Different compilers have differents have different ways of specifying the
  # out directories.
  def _Destination(self, out_dir, raw_compiler):
    pass

  def _Options(self, sources, deps):
    return []

  # Many compilers will require a companion object for special options, like
  # C++.
  def Compile(self, flags, sources, deps):
    compiler = self._Compiler()
    self._Destination(self._out_dir, compiler)
    compiler.add_flags(self._flags + flags)
    compiler.sources(sources)
    compiler.deps(deps)
    compiler.options(self._Options(sources, deps))
    compiler.Execute()

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
    compiler.Execute()
