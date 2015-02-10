from base import Rule, Executor
from java_rules import *

class BuildExecutor(Executor):
  def rule_constructors(self):
    return [java_library, java_binary]
