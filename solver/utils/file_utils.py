import os

def read_lines(filepath):
  if not os.path.exists(filepath):
    raise Exception('No file at path: {}'.format(filepath))
  lines = []

  with open(filepath, 'r') as file:
    for line in file.readlines():
      lines.append(line.replace('\n', ''))
    return lines

def write_file(filepath, content):
  with open(filepath, 'w') as file:
    file.writelines(content)

def append_conent_to_file(filepath, content):
  with open(filepath, 'a') as file:
    file.writelines(content)