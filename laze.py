from bob.builder.builder import Builder
from bob.compilers.compiler_impls import CompilerTypes, GetCompilerMapping
from bob.config.root_config import RootConfigExecutor
from bob.source_tree.dependency_graph import BuildTree
from bob.source_tree.src_tree_walker import GetAllBuildRules

def main():
  root_dir = 'ROOT'
  root_executor = RootConfigExecutor()
  config = root_executor.Execute(root_dir)[0]
  
  build_rules = GetAllBuildRules(config.src_dir)
  tree = BuildTree(dependency, build_rules)
  Builder(CompilerMapping()).Build(tree)

def CompilerMapping():
  return GetCompilerMapping({CompilerTypes.JAVA: {}})

if __name__ == "__main__":
  main()
