from compilers import Compiler

class JavaCompiler(Compiler):
  def __init__(self, compiler_path = 'java', flags = []):
    self._compiler_path = compiler_path
    self._flags = flags

  # TODO(Brendan): We should have a way to 
  def Compile(self, flags, sources):
    BuildCommand(self._compiler_path).flags(flags).args(sources).Execute()
