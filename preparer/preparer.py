import os

def init():
  working_directory = os.getcwd()
  solver_directory = os.path.join(working_directory, 'solver')
  solutions_directory = os.path.join(solver_directory, 'solutions')
  utils_directory = os.path.join(solver_directory, 'utils')
  
  create_folder(solver_directory)
  create_folder(solutions_directory)
  create_folder(utils_directory)
  create_file(solver_directory, '__init__.py')
  create_file(solutions_directory, '__init__.py')
  create_file(utils_directory, '__init__.py')

  for day in range(1, 26):
    directory_name = 'day_{}'.format(day) if day >= 10 else 'day_0{}'.format(day)
    path = os.path.join(solutions_directory, directory_name)
    data_path = os.path.join(path, 'data')

    create_folder(path)
    create_folder(data_path)

    create_file(path, '__init__.py')
    create_file(data_path, 'test.txt')
    create_file(data_path, 'data.txt')
    solve_file = os.path.join(path, 'solve.py')
    template_file = os.path.join(os.getcwd(), 'preparer', 'template.py')
    copy_file(template_file, solve_file)

def create_folder(path):
  if (not os.path.exists(path)):
    os.mkdir(path)

def create_file(path, name):
  with open(os.path.join(path, name), 'x'):
    pass

def write_file(path, name, content):
  with open(os.path.join(path, name), 'w') as file:
    file.writelines(content)

def copy_file(sourcePath, targetPath):
  with open(sourcePath, 'r') as source, open(targetPath, 'w') as target:
    for line in source:
      target.write(line)