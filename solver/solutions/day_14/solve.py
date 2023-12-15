from solver.utils.file_utils import *
import os

movement = {
  'north': (0, -1),
  'west': (-1, 0),
  'south': (0, 1),
  'east': (1, 0)
}

saved_configurations = {}

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
  rocks_data = format_data(data)
  rocks_rolled_north = roll_rocks(rocks_data, movement['north'])
  return calculate_total_load_of_rolled_rocks(rocks_data, rocks_rolled_north)

def solve_second_part(data):
  rocks_data = format_data(data)
  rocks_data['moveable_rocks'] = make_roll_cycles(rocks_data, 1000000000)
  rocks_rolled_north = roll_rocks(rocks_data, movement['north'])
  return calculate_total_load_of_rolled_rocks(rocks_data, rocks_rolled_north)

def format_data(data):
  length = len(data[0])
  height = len(data)
  moveable_rocks = []
  stable_rocks = []

  sequence = ''
  for y in range(len(data)):
    sequence += data[y]
    for x in range(len(data[y])):
      if data[y][x] == 'O':
        moveable_rocks.append(x_y_to_index((x, y), length))
      elif data[y][x] == '#':
        stable_rocks.append(x_y_to_index((x, y), length))

  return {'length': length, 'height': height, 'moveable_rocks': moveable_rocks, 'stable_rocks': stable_rocks}

def roll_rocks(rocks_data, movement):
  height = rocks_data['height']
  length = rocks_data['length']
  moveable_rocks = rocks_data['moveable_rocks'].copy()
  stable_rocks = rocks_data['stable_rocks']
  modified = True

  while modified:
    modified = False

    moveable_rocks = sort_before_movement(moveable_rocks, length, movement)

    for i in range(len(moveable_rocks)):
      rock_index = moveable_rocks[i]
      next_rock_index = move_index(rock_index, length, movement)

      if next_rock_index < 0 or next_rock_index >= length * height or (next_rock_index in moveable_rocks or next_rock_index in stable_rocks):
        continue

      moveable_rocks[i] = next_rock_index
      modified = True
  
  moveable_rocks.sort()
  return moveable_rocks

def sort_before_movement(rocks_indexes, length, movement):
  rocks_coordinations = [get_x_y_coordinates(index, length) for index in rocks_indexes]

  if movement[1] == -1:
    return sorted(rocks_indexes)
  elif movement[1] == 1:
    return sorted(rocks_indexes, reverse=True)
  elif movement[0] == 1:
    sorted_coordination = sorted(rocks_coordinations, key=lambda x:x[0], reverse=True)
    return [x_y_to_index((coord[0], coord[1]), length) for coord in sorted_coordination]
  elif movement[0] == -1:
    sorted_coordination = sorted(rocks_coordinations, key=lambda x:x[0])
    return [x_y_to_index((coord[0], coord[1]), length) for coord in sorted_coordination]

def make_roll_cycles(rocks_data, cycles_number):
  keys_path = []
  index_stopped = 0
  index = 0

  while index <= cycles_number and index_stopped == 0:
    for key in movement:
      save_key = ''.join([str(d) for d in rocks_data['moveable_rocks']])

      if save_key in keys_path:
        index_stopped = index

      keys_path.append(save_key)

      if save_key in saved_configurations:
        rocks_data['moveable_rocks'] = saved_configurations[save_key]
      else:
        rocks_data['moveable_rocks'] = roll_rocks(rocks_data, movement[key])
        saved_configurations[save_key] = rocks_data['moveable_rocks'].copy()
      print(key, calculate_total_load_of_rolled_rocks(rocks_data, rocks_data['moveable_rocks']))

    index += 1

  offset = keys_path.index(keys_path[-1])
  looped_path_length = len(keys_path) - 1 - offset
  end_position_in_cycles = cycles_number % looped_path_length
  end_key = keys_path[offset + end_position_in_cycles-1]
  print(key, calculate_total_load_of_rolled_rocks(rocks_data, saved_configurations[end_key]))
  return saved_configurations[end_key]



def calculate_total_load_of_rolled_rocks(rocks_data, rolled_rocks_indexes):
  height = rocks_data['height']
  length = rocks_data['length']
  rolled_rocks_coordinations = [get_x_y_coordinates(index, length) for index in rolled_rocks_indexes]

  sum = 0
  for row in range(height):
    weight = height - row
    rocks_number = len([rock for rock in rolled_rocks_coordinations if rock[1] == row])

    sum += weight * rocks_number

  return sum


def get_x_y_coordinates(index, row_length):
  x = index % row_length
  y = int((index - x) / row_length)

  return (x, y)

def x_y_to_index(coordinates, row_length):
  return int(coordinates[0] + (coordinates[1] * row_length))

def move_index(index, length, move):
  (x, y) = get_x_y_coordinates(index, length)
  if x + move[0] < 0 or x + move[0] >= length:
    return index
  return x_y_to_index((x + move[0], y + move[1]), length)

def print_map(moveable_rocks, stable_rocks, length, height):
  sequence = ''
  index = 0

  while index < height * length:
    if index % length == 0:
      print(sequence)
      sequence = ''

    if index in moveable_rocks:
      sequence += 'O'
    elif index in stable_rocks:
      sequence += '#'
    else:
      sequence += '.'
    index += 1
  print(sequence)