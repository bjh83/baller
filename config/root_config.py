from base import Rule, Executor

class root_config(Rule):
  def __init__(self):
    self.src_dir = None
    self.extern_deps = None
    self.cpp_flags = None

class RootConfigExecutor(Executor):
  def rule_constructors(self):
    return [root_config]
