from base import Rule

class java_library(Rule):
  def __init__(self):
    self.name = None
    self.srcs = []
    self.deps = []

class java_binary(Rule):
  def __init__(self):
    self.name = None
    self.srcs = []
    self.deps = []
