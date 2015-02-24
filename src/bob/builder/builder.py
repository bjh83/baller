from bob.source_tree.dependency_graph import BuildTree, DependencyTreeNode

import os

class Builder:
  def __init__(self, compiler_mapping):
    self._compiler_mapping = compiler_mapping
    self._compiled_rules = {}
    
  def Build(self, tree):
    indices = range(tree.MaxDepth())
    indices.reverse()
    for i in indices:
      nodes_to_build = tree.ChildrenAtDepth(i)
      for node in nodes_to_build:
        build_rule = node.value
        rule_path = node.name
        if rule_path not in self._compiled_rules:
          self.BuildRule(rule_path, build_rule)
  
  def BuildRule(self, rule_path, build_rule):
    compiler = self._GetCompiler(build_rule)
    dependencies = self._GetDependencies(build_rule)
    compiled_rules = compiler.Compile(rule_path, build_rule, dependencies)
    self._compiled_rules[rule_path] = compiled_rules

  def _GetDependencies(self, build_rule):
    return [self._compiled_rules[rule] for rule in build_rule.deps]

  def _GetCompiler(self, build_rule):
    return self._compiler_mapping[build_rule.compiler()]
