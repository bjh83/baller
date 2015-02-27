class CompiledObject(object):
  def __init__(self, components):
    self.components = components

class JavaCompiledObject(CompiledObject):
  pass

class CppCompiledObject(CompiledObject):
  def __init__(self, hdrs, objs):
    self.hdrs = hdrs
    self.objs = objs
