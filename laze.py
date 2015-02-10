from root_config import RootConfigExecutor

def main():
  root_dir = 'ROOT'
  root_executor = RootConfigExecutor()
  config = root_config.Execute(root_dir)


if __name__ == "__main__":
  main()
