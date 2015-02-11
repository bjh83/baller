from dependency_graph import BuildTree, DependencyTreeNode

def Build(tree):
  for i in range(tree.MaxDepth()).reverse():
    nodes_to_build = tree.ChildrenAtDepth(i)
    for node in nodes_to_build:
      build_rule = node.value
      build_rule.Compile()
