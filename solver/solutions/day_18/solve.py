from solver.utils.file_utils import *
import os
import re

movements = {
  'R': (1, 0),
  'L': (-1, 0),
  'U': (0, -1),
  'D': (0, 1)
}

length = None
height = None

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
  instructions = format_data(data)
  start_point = {'position': (0, 0), 'color': None}
  points = execute_instructions(start_point, instructions)
  normalize_points(points)
  points += fill_points_inside(points)
  # cubics = get_cubics(points)
  print_map(points)
  return len(points)

def solve_second_part(data):
  pass

def format_data(data):
  instructions = []
  for line in data:
    [direction, length, color] = line.split(' ')
    color = re.sub(r'[\(\)]', '', color)
    instructions.append({'direction': direction, 'length': int(length), 'color': color})
  return instructions

def execute_instructions(origin, instructions):
  last_origin = origin
  result_points = [origin]
  for instruction in instructions:
    for step in range(instruction['length']):
      movement = movements[instruction['direction']]
      new_position = move_position(last_origin['position'], movement)
      last_origin = {'position': new_position, 'color': instruction['color']}
      has_position_already = [position for position in result_points if position['position'][0] == new_position[0] and position['position'][1] == new_position[1]]
      if len(has_position_already) == 0:
        result_points.append(last_origin)
  return result_points

def normalize_points(points):
  min_x = get_min_x_from_points(points)
  min_y = get_min_y_from_points(points)
  max_x = get_max_x_from_points(points)
  max_y = get_max_y_from_points(points)

  x_diff = 0 - min_x
  y_diff = 0 - min_y

  global length
  global height

  length = x_diff + max_x + 1
  height = y_diff + max_y + 1

  for point in points:
    (x, y) = point['position']
    point['position'] = (x + x_diff, y + y_diff)

def fill_points_inside(points):
  map_size = length * height
  filled_positions = []
  print(map_size)

  for i in range(map_size):
    percentage = i / map_size * 100
    print(percentage)
    position = index_to_x_y(i, length)
    if has_points_around(position, points) and not is_position_in_points(position, points):
      filled_positions.append(position)
  
  return [{'position': position, 'color': None} for position in filled_positions]

def is_position_in_points(position, points):
  for point in points:
    if position[0] == point['position'][0] and position[1] == point['position'][1]:
      return True
  return False

def has_points_around(position, points):
  up, down, left, right = None, None, None, None

  for point in points:
    if point['position'][0] == position[0] and point['position'][1] == position[1]:
      continue
    elif point['position'][0] == position[0] and point['position'][1] < position[1]:
      up = point
    elif point['position'][0] == position[0] and point['position'][1] > position[1]:
      down = point
    elif point['position'][1] == position[1] and point['position'][0] < position[0]:
      left = point
    elif point['position'][1] == position[1] and point['position'][0] > position[0]:
      right = point
  return True if up and down and left and right else False

def get_cubics(points):
  sorted_points = sorted(points, key=lambda x: x_y_to_index(x['position'], length), reverse=True)
  row_cubics = []
  while len(sorted_points) > 0:
    point = sorted_points.pop()
    row_cubic = [point]
    current_point = point
    while True:
      next_position = move_position(current_point['position'], movements['R'])
      point_index = get_point_index_at(next_position, sorted_points)

      if point_index == None:
        break
      current_point = sorted_points.pop(point_index)
      row_cubic.append(current_point)

    if len(row_cubic):
      row_cubics.append(sorted(row_cubic, key=lambda x: x['position'][0]))
  
  join_row_cubics(row_cubics)

def join_row_cubics(row_cubics):
  copy_row_cubics = sorted(row_cubics.copy(), key=lambda x:x[0]['position'][1], reverse=True)
  cubics = []

  while len(copy_row_cubics) > 0:
    current_row = copy_row_cubics.pop()
    cols = [current_row]
    rows_with_same_length = [row for row in copy_row_cubics if len(row) == len(current_row)]

    while current_row:
      for i in range(len(rows_with_same_length)):
        has_same_start_x = rows_with_same_length[i][0]['position'][0] == current_row[0]['position'][0]
        has_same_end_x = rows_with_same_length[i][-1]['position'][0] == current_row[-1]['position'][0]
        is_next = rows_with_same_length[i][0]['position'][1] == current_row[0]['position'][1] + 1

        if has_same_start_x and has_same_end_x and is_next:
          row = rows_with_same_length[i]
          copy_row_cubics.remove(row)
          cols.append(row)
          current_row = row
          break
      else:
        current_row = None
    if len(cols):
      cubics.append(cols)
  

def get_point_index_at(position, points):
  for i in range(len(points)):
    if points[i]['position'][0] == position[0] and points[i]['position'][1] == position[1]:
      return i
  return None

def get_min_x_from_points(points):
  min_x = 1000000000000000
  for point in points:
    (x, y) = point['position']
    if min_x > x:
      min_x = x
  return min_x

def get_min_y_from_points(points):
  min_y = 1000000000000000
  for point in points:
    (x, y) = point['position']
    if min_y > y:
      min_y = y
  return min_y

def get_max_x_from_points(points):
  max_x = -1000000000000000
  for point in points:
    (x, y) = point['position']
    if max_x < x:
      max_x = x
  return max_x

def get_max_y_from_points(points):
  max_y = -1000000000000000
  for point in points:
    (x, y) = point['position']
    if max_y < y:
      max_y = y
  return max_y

def move_position(position, movement):
  return (position[0] + movement[0], position[1] + movement[1])

def index_to_x_y(index, row_length):
  x = index % row_length
  y = int((index - x) / row_length)
  return (x, y)

def x_y_to_index(coordinates, row_length):
  return int(coordinates[0] + (coordinates[1] * row_length))

def print_map(points):
  digs = [x_y_to_index(point['position'], length) for point in points]

  ground = ['.' for index in range(length * height)]

  for i in range(len(ground)):
    if i in digs:
      ground[i] = '#'
  
  for y in range(height):
    sequence = ''
    for x in range(length):
      sequence += ground[x_y_to_index((x, y), length)]
    print(sequence)