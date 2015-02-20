from bob.rules.build_rules import BuildExecutor
import os

class SourceTreeNode:
  def __init__(self, folder_name = '', children = []):
    self.folder_name = folder_name
    self.children = children

def WalkDirectory(root):
  print 'WalkDirectory:root = ' + str(root)
  children = []
  print 'WalkDirectory:dirs = ' + str(os.listdir(root))
  os.chdir(root)
  for directory in os.listdir('.'):
    if os.path.isdir(directory):
      print 'WalkDirectory:directory = ' + str(directory)
      children.append(WalkDirectory(directory))
  os.chdir('..')
  return SourceTreeNode(root, children)

def GenerateDirectoryPaths(tree_node):
  full_paths = [tree_node.folder_name]
  print 'GenerateDirectoryPaths:tree_node.children = ' + str(tree_node.children)
  for child in tree_node.children:
    for subdir in GenerateDirectoryPaths(child):
      print 'GenerateBuildPaths:file_name = ' + str(subdir)
      full_paths.append(tree_node.folder_name + os.sep + subdir)
  return full_paths

def GenerateBuildPaths(directory_paths):
  print 'GenerateBuildPaths:directory_paths = ' + str(directory_paths)
  build_paths = []
  for directory_path in directory_paths:
    build_path = directory_path + os.sep + 'BUILD'
    if os.path.isfile(build_path):
      build_paths.append(directory_path)
  return build_paths

def GetBuildRules(build_paths):
  print 'GetBuildRules:build_paths = ' + str(build_paths)
  build_executor = BuildExecutor()
  build_rules = {}
  for build_path in build_paths:
    local_rules = build_executor.Execute(build_path + os.sep + 'BUILD')
    for rule in local_rules:
      global_name = '//' + build_path + ':' + rule.name
      build_rules[global_name] = rule
  return build_rules

def GetAllBuildRules(root):
  source_tree = WalkDirectory(root)
  build_paths = GenerateBuildPaths(GenerateDirectoryPaths(source_tree))
  return GetBuildRules(build_paths)
