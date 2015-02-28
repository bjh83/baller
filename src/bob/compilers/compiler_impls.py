from bob.commandline.commandline import ExecuteCommand
from bob.compilers.base_compiler import Compiler, RawCompiler, AbsolutePath, DecomposeDep
from bob.compiled_objects.compiled_objects import JavaCompiledObject, CppCompiledObject

import os

class CompilerTypes:
  JAVA = 'java'
  CPP = 'cpp'

def GetCompilerMapping(compiler_options):
  return {
      CompilerTypes.JAVA: JavaCompiler(**compiler_options[CompilerTypes.JAVA]),
      CompilerTypes.CPP: CPPCompiler(**compiler_options[CompilerTypes.CPP]),
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

class CPPCompiler(Compiler):
  def __init__(self, flags = [], src_dir = 'src', out_dir = 'out'):
    super(CPPCompiler, self).__init__(flags, out_dir, src_dir)

  def _CompiledObject(self, rule_path, build_rule):
    src_path = AbsolutePath(self._src_dir)
    out_path = AbsolutePath(self._out_dir)
    srcs = self._GetSources(rule_path, build_rule)
    hdrs = self._GetHeaders(rule_path, build_rule)

    srcs = [src.replace('.cc', '.o').replace(src_path, out_path) for src in srcs]
    return CppCompiledObject(hdrs, srcs)

  # TODO(Brendan): We should have a way to limit sources and headers to those in
  # the srcs, hdrs, and deps.
  def _AddDependencies(self, dependencies, raw_compiler):
    raw_compiler.add_flags(['-I' + AbsolutePath(self._src_dir)])

  def _GetHeaders(self, dep_name, build_rule):
    rule_path, _ = DecomposeDep(dep_name)
    return [AbsolutePath(rule_path + os.sep + source) for source in build_rule.hdrs]

  # TODO(Brendan): Should be able to change the compiler path.
  def _Compiler(self):
    return ExecuteCommand('g++')

  # TODO(Brendan): We should probably set the destination to the full path of
  # the source to be compiled.
  def _Destination(self, out_dir, raw_compiler):
    raw_compiler.destination(out_dir)

  def _ObjectName(self, source):
    src_path = AbsolutePath(self._src_dir)
    out_path = AbsolutePath(self._out_dir)
    return source.replace('.cc', '.o').replace(src_path, out_path)

  def _CompileSource(self, source):
    obj_name = self._ObjectName(source)
    GenerateDirectoryForObject(obj_name)
    raw_compiler = self._Compiler()
    raw_compiler.flags([])
    raw_compiler.args(['-c', source, '-o', obj_name])

  def Compile(self, rule_path, build_rule, dependencies):
    compiler = self._Compiler()
    for src in self._GetSources(rule_path, build_rule):
      self._CompileSource(src)
    return self._CompiledObject(rule_path, build_rule)

def GenerateDirectoryForObject(full_path):
  path = os.path.dirname(full_path)
  if not os.path.isdir(path):
    os.makedirs(path)
