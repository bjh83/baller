from root_config import RootConfigExecutor

def main():
  root_dir = 'ROOT'
  root_executor = RootConfigExecutor()
  config = root_executor.Execute(root_dir)
  print str(config)


if __name__ == "__main__":
  main()
