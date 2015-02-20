from bob.compilers.base_compiler import Compiler, RawCompiler

class CompilerTypes:
  JAVA = 'java',

def GetCompilerMapping(compiler_options):
  return {
      JAVA: JavaCompiler(**compiler_options[JAVA])
  }

class JavaCompiler(Compiler):
  def __init__(self, flags = [], out_dir = 'out'):
    self._flags = flags
    self._out_dir = out_dir

  def _Compiler(self):
    return RawCompiler('javac')

  def _Destination(self, out_dir, raw_compiler):
    dest_flag = '-d ' + out_dir
    raw_compiler.add_flags([dest_flag])
