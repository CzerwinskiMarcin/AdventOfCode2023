from solver.utils.file_utils import *
import os
import re

instruction_map = {
  'L': 0,
  'R': 1
}

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
  return count_steps('AAA', 'ZZZ', data)

def solve_second_part(data):
  data = format_data(data)
  origins = [map['origin'] for map in data['maps'] if re.match(r'..A', map['origin'])]
  paths_data  = [define_loop_paths_data(origin, data) for origin in origins]
  print(paths_data)
  return
  return calculate_ending_points(paths_data)

def format_data(data):
  d = [x for x in data if x != '']
  instructions = [instruction_map[direction] for direction in d[0]]
  maps = []
  for i in range(len(d) - 1):
    line = d[i+1].replace(' = ', ';').replace('(', '').replace(')', '').replace(' ', '')
    [origin, raw_destinations] = line.split(';')
    destinations = raw_destinations.split(',')
    map_part = {'origin': origin, 'destinations': destinations}
    maps.append(map_part)
  return {'instructions': instructions, 'maps': maps}

def count_steps(origin, end, data):
  instructions = data['instructions']
  maps = data['maps']
  is_at_end = False
  steps = 0

  while not is_at_end:
    steps += 1
    destination = make_step(origin, maps, steps, instructions)

    is_at_end = destination == end
    origin = destination

  return steps

def find_map_with_origin(origin, maps):
  return [map for map in maps if map['origin'] == origin][0]

def make_step(origin, maps, step_number, instructions):
    current_direction = instructions[step_number % len(instructions) - 1]
    current_map = find_map_with_origin(origin, maps)
    return current_map['destinations'][current_direction]
  
def define_loop_paths_data(origin, data):
  maps = data['maps']
  instructions = data['instructions']
  path = []
  looped = False
  was_at_end = False
  step = 0
  loop_enter = None

  while not looped:
    step += 1
    next_position = make_step(origin, maps, step, instructions)
    origin = next_position

    if was_at_end:
      loop_enter = next_position
      looped = True
    else:
      path.append(next_position)

    if re.match(r'..Z', next_position):
      was_at_end = True
  
  loop_offset = path.index(loop_enter)
  path_length = len(path) - loop_offset

  return {'offset': loop_offset, 'length': path_length}

def calculate_ending_points(paths_data):
  for path_data in paths_data:
    path_data['end_position_step'] = path_data['offset'] + path_data['length']

  all_at_end = False

  while not all_at_end:
    min_pos_path = min(paths_data, key=get_end_position_step)
    min_pos_path['end_position_step'] += min_pos_path['length']
    all_at_end = all(path['end_position_step'] == min_pos_path['end_position_step'] for path in paths_data)
    print(min_pos_path['end_position_step'])
  
  return paths_data[0]['end_position_step']

def get_end_position_step(path_data):
  return path_data['end_position_step']