from solver.utils.file_utils import *
import os

def solve(type, part):
  target_data_file = 'test.txt' if type == 'test' else 'data.txt'
  solve_directory_path = os.path.dirname(__file__)
  filepath = os.path.join(solve_directory_path, 'data', target_data_file)
  data = read_lines(filepath)
  return do_solve(part, data)

def do_solve(part, data):
  if part == 'first':
    return solve_first_part(data)
  else:
    return solve_second_part(data)

def solve_first_part(data):
  data = format_data(data)
  vertical_symmetries = [find_vertical_symmetry(map_data) for map_data in data]
  horizontal_symmetries = [find_horizontal_symmetry(map_data) for map_data in data]

  vertical_symmetries = [point for point in vertical_symmetries if point != None]
  horizontal_symmetries = [point for point in horizontal_symmetries if point != None]

  patterns_horizontal = [int(point * 100) for point in horizontal_symmetries]
  patterns_vertical = [int(point) for point in vertical_symmetries]
  return sum(patterns_vertical + patterns_horizontal)


def solve_second_part(data):
  pass

def format_data(data):
  maps = []

  map_data = {'map': '', 'length': None, 'height': None}
  map_height = 0
  for line in data:
    if line != '':
      map_data['length'] = len(line)
      map_data['map'] += line
      map_height += 1
    else:
      map_data['height'] = map_height
      map_height = 0
      maps.append(map_data)
      map_data = {'map': '', 'length': None, 'height': None}
  map_data['height'] = map_height
  maps.append(map_data)
  return maps

def find_vertical_symmetry(map_data):
  map = map_data['map']
  length = map_data['length']
  height = map_data['height']
  for x in range(map_data['length'] - 1):
    left_col_chars = get_map_col(map, x, length, height) 
    right_col_chars = get_map_col(map, x + 1, length, height) 

    are_symmetric = are_sequences_same(left_col_chars, right_col_chars)

    if are_symmetric and check_symmetricity_of_vertical(map_data, x):
      return x + 1

  
def check_symmetricity_of_vertical(map_data, left_symmerty_point):
  map = map_data['map']
  length = map_data['length']
  height = map_data['height']

  step = None
  start_point = None
  end_point = None
  count = 0

  if int(length / 2) > left_symmerty_point:
    step = -1
    start_point = left_symmerty_point
    end_point = 0
  else:
    step = 1
    start_point = left_symmerty_point + 1
    end_point = length - 1

  mirrored_step = int(step * -1)

  while True:
    current_step = start_point + count * step
    current_mirrored_step = start_point + mirrored_step + count * mirrored_step
    first_col = get_map_col(map, current_step, length, height)
    second_col = get_map_col(map, current_mirrored_step, length, height)
    are_same = are_sequences_same(first_col, second_col)
    
    if not are_same:
      return False
    elif current_step == end_point:
      break

    count += 1

  return True

def find_horizontal_symmetry(map_data):
  map = map_data['map']
  length = map_data['length']
  height = map_data['height']

  for y in range(height - 1):
    up_row_chars = get_map_row(map, y, length, height) 
    down_row_chars = get_map_row(map, y+1, length, height)
    are_same = are_sequences_same(up_row_chars, down_row_chars)

    if are_same and check_horizontal_symetry(map_data, y):
      return y + 1

def check_horizontal_symetry(map_data, up_symmetry_point):
  map = map_data['map']
  length = map_data['length']
  height = map_data['height']

  count = 0
  step = None
  mirrored_step = None
  start_point = None
  end_point = None

  if int(height/2) > up_symmetry_point:
    start_point = up_symmetry_point
    end_point = 0
    step = -1
  else:
    start_point = up_symmetry_point + 1
    end_point = height - 1
    step = 1
  
  mirrored_step = int(step * -1)

  while True:
    current_step = start_point + count * step
    current_mirrored_step = start_point + mirrored_step + count * mirrored_step

    first_row = get_map_row(map, current_step, length, height)
    second_row = get_map_row(map, current_mirrored_step, length, height)
    are_same = are_sequences_same(first_row, second_row)

    if not are_same:
      return False

    count += 1

    if current_step == end_point:
      break
  
  return True

def get_map_col(map, x, length, height):
  col = []
  for y in range(height):
    col.append(map[x_y_to_index((x, y), length)])
  return col

def get_map_row(map, y, length, height):
  row = []
  for x in range(length):
    row.append(map[x_y_to_index((x, y), length)])
  return row

def are_sequences_same(first, second):
    return all([first[i] == second[i] for i in range(len(first))])

def get_x_y_coordinates(index, row_length):
  x = index % row_length
  y = (index - x) / row_length

  return (x, y)

def x_y_to_index(coordinates, row_length):
  return int(coordinates[0] + (coordinates[1] * row_length))