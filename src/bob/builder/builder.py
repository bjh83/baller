from bob.source_tree.dependency_graph import BuildTree, DependencyTreeNode

class Builder:
  def __init__(self, compiler_mapping):
    self._compiler_mapping = compiler_mapping
    
  def Build(self, tree):
    for i in range(tree.MaxDepth()).reverse():
      nodes_to_build = tree.ChildrenAtDepth(i)
      for node in nodes_to_build:
        build_rule = node.value
        BuildRule(build_rule)
  
  def BuildRule(self, build_rule):
    flags = build_rule.flags
    sources = self._GetSources(build_rule)
    dependencies = self._GetDependencies(build_rule)
    compiler = self._GetCompiler(build_rule)
    compiler.Compile(flags, sources, dependencies)

  def _GetSources(self, build_rule):
    return [AbsolutePath(source) for source in build_rule.srcs]

  # TODO(Brendan): Do something appropriate here!!!
  def _GetDependencies(self, build_rule):
    return []

  def _GetCompiler(self, buid_rule):
    return self._compiler_mapping[build_rule.compiler()]
