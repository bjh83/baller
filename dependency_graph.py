class DependencyTreeNode:
  def __init__(self, name, value, children):
    self.name = name
    self.value = value
    self.children = children

  def MaxDepth(self):
    if len(children) == 0:
      return 1
    else:
      return max([child.MaxDepth() for child in children]) + 1

  def ChildrenAtDepth(self, index):
    if index > 0:
      return [sub_child for child in self.children \
          for sub_child in child.ChildrenAtDepth(index - 1)]
    else:
      return [self]

def BuildTree(dependency, build_rules, calculated_dependencies = []):
  # TODO(Brendan): Make better exceptions.
  if dependency not in build_rules:
    raise Exception('Build rule: ' + dependency + ' does not exist')
  elif dependency in calculated_dependencies:
    # TODO(Brendan): Give the conflict. (Could be done with a map to the
    # previous user of the dependency.)
    raise Exception('Circular dependency: ' + dependency)

  calculated_dependencies.append(dependency)
  build_rule = build_rules[dependency]

  children = []
  for sub_dep in build_rule.deps:
    node = BuildTree(sub_dep, build_rules, calculated_dependencies)
    children.append(node)

  calculated_dependencies.remove(dependency)
  return DependencyTreeNode(dependency, build_rule, children)

def NeedCompilation(build_rules, does_need_compilation):
  return [dep for dep, rule in build_rules.items() \
      if does_need_compilation(rule)]
