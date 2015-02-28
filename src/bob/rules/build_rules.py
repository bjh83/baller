from bob.compilers.compiler_impls import CompilerTypes
from bob.parser.base import Rule, Executor

class BuildExecutor(Executor):
  def rule_constructors(self):
    return [java_library, java_binary, cc_library, cc_binary]

# All build rule implementations should inherit from this instead of Rule. This
# is because all rules should have the fields declared below. Rule itself
# cannot declare these fields (see the parser explanation).
class RuleBase(Rule):
  def __init__(self):
    self.name = None
    self.srcs = []
    self.deps = []
    self.flags = []
    
class JavaBase(RuleBase):
  def __init__(self):
    super(JavaBase, self).__init__()

  def compiler(self):
    return CompilerTypes.JAVA

class java_library(JavaBase):
  pass

class java_binary(JavaBase):
  pass

class CCBase(RuleBase):
  def __init__(self):
    super(CCBase, self).__init__()
    self.hdrs = []

  def compiler(self):
    return CompilerTypes.CPP

class cc_library(CCBase):
  pass

class cc_binary(CCBase):
  def is_binary(self):
    return True
