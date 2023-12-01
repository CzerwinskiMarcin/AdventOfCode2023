import os

def read_lines(filepath):
  if not os.path.exists(filepath):
    raise Exception('No file at path: {}'.format(filepath))
  lines = []

  with open(filepath, 'r') as file:
    for line in file.readlines():
      lines.append(line.replace('\n', ''))
    return lines