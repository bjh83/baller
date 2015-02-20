from bob.source_tree.dependency_graph import BuildTree, DependencyTreeNode

import os

class Builder:
  def __init__(self, compiler_mapping):
    self._compiler_mapping = compiler_mapping
    
  def Build(self, tree):
    indices = range(tree.MaxDepth())
    indices.reverse()
    for i in indices:
      nodes_to_build = tree.ChildrenAtDepth(i)
      for node in nodes_to_build:
        build_rule = node.value
        dep_name = node.name
        self.BuildRule(dep_name, build_rule)
  
  def BuildRule(self, dep_name, build_rule):
    flags = build_rule.flags
    sources = self._GetSources(dep_name, build_rule)
    dependencies = self._GetDependencies(build_rule)
    compiler = self._GetCompiler(build_rule)
    compiler.Compile(flags, sources, dependencies)

  def _GetSources(self, dep_name, build_rule):
    rule_path, _ = DecomposeDep(dep_name)
    return [AbsolutePath(rule_path + os.sep + source) for source in build_rule.srcs]

  # TODO(Brendan): Do something appropriate here!!!
  def _GetDependencies(self, build_rule):
    return []

  def _GetCompiler(self, build_rule):
    return self._compiler_mapping[build_rule.compiler()]

def AbsolutePath(local_path):
  return os.path.abspath(local_path)

def DecomposeDep(dep_name):
  [path, rule_name] = dep_name.strip('//').split(':')
  return path, rule_name
