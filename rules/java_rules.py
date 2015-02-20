from bob.compilers.compiler_impls import CompilerTypes
from bob.rules.build_rules import RuleBase

class JavaBase(RuleBase):
  def __init__(self):
    super(self, RuleBase).__init__()

  def compiler(self):
    return CompilerTypes.JAVA

class java_library(JavaBase):
  pass

class java_binary(JavaBase):
  pass
