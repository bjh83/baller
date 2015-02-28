import __builtin__

# This class should not be overriden except by RuleBase. It is used to define
# what fields should be ignored when parsing BUILD files.
class Rule(object):
  def __init__(self):
    pass

  def __str__(self):
    fields = self.fields()
    string = self.__class__.__name__ + '('
    for field in fields:
      string = string + field + ' = ' + str(getattr(self, field)) + ', '
    string = string + ')'
    return string

  def __repr__(self):
    return str(self)

  def fields(self):
    return set(dir(self)) - set(dir(Rule()))

  # Defines the compiler type used for compiling these files.
  def compiler(self):
    pass

  def is_binary(self):
    return False

  def Validate(self):
    for field in self.fields():
      if getattr(self, field) is None:
        raise ValueError(field + ' is required and was not set.')

# This BUILD rule parser. We use python's interpretter as our parser; this works
# by mapping a Rule (defined above) to a magic method that creates and adds a
# rule to a list when called. The build rules in a build file are actually calls
# to these magic methods.
class Executor:
  def __init__(self):
    self._rules = {}
    self._results = []
    self._CreateRules()

  # Override this to return the appropriate rules.
  def rule_constructors(self):
    pass

  def Execute(self, file_name):
    self._results = []
    self._ExecuteFile(file_name)
    return self._results

  def _CreateRules(self):
    for constructor in self.rule_constructors():
      func = self._CreateRule(constructor)
      self._rules[constructor.__name__] = func

  def _CreateRule(self, constructor):
    field_names = constructor().fields()
    def func(**kwargs):
      rule = constructor()
      for name, value in kwargs.items():
        if name in field_names:
          setattr(rule, name, value)
        else:
          raise AttributeError(constructor.__name__ + " has no attribute '" + name + "'")
      rule.Validate()
      self._results.append(rule)
    return func

  def __enter__(self):
    for name, function in self._rules.items():
      setattr(__builtin__, name, function)

  def __exit__(self, type, value, traceback):
    for name in self._rules.keys():
      delattr(__builtin__, name)

  def _ExecuteFile(self, file_name):
    with self:
      execfile(file_name)
