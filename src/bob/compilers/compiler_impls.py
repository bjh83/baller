from bob.compilers.base_compiler import Compiler, RawCompiler, AbsolutePath
from bob.compiled_objects.compiled_objects import JavaCompiledObject

import os

class CompilerTypes:
  JAVA = 'java',

def GetCompilerMapping(compiler_options):
  return {
      CompilerTypes.JAVA: JavaCompiler(**compiler_options[CompilerTypes.JAVA])
  }

class JavaCompiler(Compiler):
  def __init__(self, flags = [], out_dir = 'out', src_dir = 'src', class_path = None):
    self._flags = flags
    self._out_dir = out_dir
    self._src_dir = src_dir
    if class_path is None:
      class_path = os.path.join(src_dir, 'main/java')
    self._class_path = class_path

  def _CompiledObject(self, rule_path, build_rule):
    src_path = AbsolutePath(self._src_dir)
    out_path = AbsolutePath(self._out_dir)
    srcs = [src for src in self._GetSources(rule_path, build_rule)]
    return JavaCompiledObject([src.replace('.java', '.class').replace(src_path,
      out_path) for src in srcs])

  def _AddDependencies(self, dependencies, raw_compiler):
    raw_compiler.add_flags(['-classpath ' + self._class_path])

  def _Compiler(self):
    return RawCompiler('javac')

  def _Destination(self, out_dir, raw_compiler):
    dest_flag = '-d ' + out_dir
    raw_compiler.add_flags([dest_flag])
