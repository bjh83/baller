class Compiler:
  def __init__(self, flags):
    self.flags = flags

  # Many compilers will require a companion object for special options, like
  # C++.
  def Compile(self, options, sources):
    pass

class RawCompiler:
  def __init__(self, compiler_path):
    self._compiler_path = compiler_path

  def flags(self, flags):
    self._flags = flags
    return self

  # For some compilers there are special flags which should be treated
  # differently (like C++ and -I).
  def options(self, options):
    return self

  def sources(self, sources):
    self._sources = sources
    return self

  # Different compilers will likely have 
  def destination(self, destination):
    return self
