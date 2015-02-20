from bob.parser.base import Rule, Executor

class root_config(Rule):
  def __init__(self):
    self.src_dir = None
    self.extern_deps = []
    self.cpp_flags = []

class RootConfigExecutor(Executor):
  def rule_constructors(self):
    return [root_config]
