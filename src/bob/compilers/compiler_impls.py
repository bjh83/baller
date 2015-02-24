from bob.compilers.base_compiler import Compiler, RawCompiler

class CompilerTypes:
  JAVA = 'java',

def GetCompilerMapping(compiler_options):
  return {
      CompilerTypes.JAVA: JavaCompiler(**compiler_options[CompilerTypes.JAVA])
  }

class JavaCompiler(Compiler):
  def __init__(self, flags = [], out_dir = 'out'):
    self._flags = flags
    self._out_dir = out_dir

  def _CompiledObject(self, rule_path, build_rule):
    return JavaCompiledObject([source.replace('.java', '.class') \
        for source in self._GetSources(rule_path, build_rule)])

  def _Compiler(self):
    return RawCompiler('javac')

  def _Destination(self, out_dir, raw_compiler):
    dest_flag = '-d ' + out_dir
    raw_compiler.add_flags([dest_flag])
