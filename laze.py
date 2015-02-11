from dependency_graph import BuildTree
from root_config import RootConfigExecutor
from src_tree_walker import GetAllBuildRules

def main():
  root_dir = 'ROOT'
  root_executor = RootConfigExecutor()
  config = root_executor.Execute(root_dir)[0]
  
  build_rules = GetAllBuildRules(config.src_dir)
  tree = BuildTree(dependency, build_rules)
  Build(tree)


if __name__ == "__main__":
  main()
