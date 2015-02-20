import os, subprocess

class ExecuteCommand(object):
  def __init__(self, command_name):
    self._command_name = command_name

  def flags(self, flags):
    self._flags = flags

  def args(self, args):
    self._args = args

  def Execute(self):
    command_list = [self._command_name] + self._flags + self._args
    command = ' '.join(command_list)
    return_code = subprocess.call(command, shell=True)

class ExecuteContextualCommand(ExecuteCommand):
  def __init__(self, command_name):
    self._command_name = command_name

  def before(self):
    pass

  def after(self):
    pass

  def __enter__(self):
    self.before()

  def __exit__(self, type, value, traceback):
    self.after()

  def Execute(self):
    with self:
      super(ExecuteContextualCommand, self).Execute()

class ExecuteCommandInDirectory(ExecuteContextualCommand):
  def directory(self, path):
    self._path = path

  def before(self):
    self._original_location = os.getcwd()
    os.chdir(self._path)

  def after(self):
    os.chdir(self._original_location)
