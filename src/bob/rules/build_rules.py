from bob.parser.base import Rule, Executor
from bob.rules.java_rules import *

class BuildExecutor(Executor):
  def rule_constructors(self):
    return [java_library, java_binary]

# All build rule implementations should inherit from this instead of Rule. This
# is because all rules should have the fields declared below. Rule itself
# cannot declare these fields (see the parser explanation).
class RuleBase(Rule):
  def __init__(self):
    self.name = None
    self.srcs = []
    self.deps = []
