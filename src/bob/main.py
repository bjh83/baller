from bob.builder.builder import Builder
from bob.compilers.compiler_impls import CompilerTypes, GetCompilerMapping
from bob.config.root_config import RootConfigExecutor
from bob.source_tree.dependency_graph import BuildTree
from bob.source_tree.src_tree_walker import GetAllBuildRules

from os import path
import sys

def main(args = sys.argv):
  root_file = 'ROOT'
  if len(args) != 2:
    print 'Please specify the dependency form path for your build.'
    return
  dependency = args[1]

  CheckForROOT(root_file)
  root_executor = RootConfigExecutor()
  config = root_executor.Execute(root_file)[0]
  
  build_rules = GetAllBuildRules(config.src_dir)
  tree = BuildTree(dependency, build_rules)
  Builder(CompilerMapping(config)).Build(tree)

def CompilerMapping(config):
  return GetCompilerMapping({
    CompilerTypes.JAVA: {'out_dir': config.out_dir},
    CompilerTypes.CPP: {},
    })

def CheckForROOT(root_file):
  if not path.isfile(root_file):
    raise ValueError(root_file + " does not exist")
