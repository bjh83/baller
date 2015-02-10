from build_rules import BuildExecutor
import os

class SourceTreeNode:
  def __init__(self, folder_name = '', children = []):
    self.folder_name = folder_name
    self.children = children

def WalkDirectory(root):
  children = []
  for directory in os.listdir(root) if os.path.isdir(directory):
    os.chdir(directory)
    children.append(WalkDirectory(directory))
    os.chdir('..')
  return SourceTreeNode(root, children)

def GenerateDirectoryPaths(tree_node):
  return [tree_node.folder_name + os.pathsep + GenerateDirectoryPaths(child) \
      for child in tree_node.children] + tree_node.folder_name

def GenerateBuildPaths(directory_paths):
  build_paths = []
  for directory_path in directory_paths:
    build_path = directory_path + os.pathsep + 'BUILD'
    if os.path.isfile(build_path):
      build_paths.append(build_path)
  return build_paths

def GetBuildRules(build_paths):
  build_executor = BuildExecutor()
  build_rules = []
  for build_path in build_paths:
    build_rules.extend(build_executor.Execute(build_path))
  return build_rules

def GetAllBuildRules(root):
  source_tree = WalkDirectory(root)
  build_paths = GenerateBuildPaths(GenerateDirectoryPaths(source_tree))
  return GetBuildRules(build_paths)
