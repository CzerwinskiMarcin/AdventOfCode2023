from solver.utils.file_utils import *
import os

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
  pass

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
    # print('Step', steps)
    current_direction = instructions[steps % len(instructions) - 1]
    # print(f'\tInstructions: {instructions}')
    # print(f'\tCurrent direction index: {steps % len(instructions)}')
    # print(f'\tCurrent direction: {instructions[steps % len(instructions)]}')
    current_map = find_map_with_origin(origin, maps)
    # print(f'\tCurrent map {current_map}')
    destination = current_map['destinations'][current_direction]
    # print(f'\tDestination: {destination}')

    is_at_end = destination == end
    origin = destination
    # print()

  return steps

def find_map_with_origin(origin, maps):
  return [map for map in maps if map['origin'] == origin][0]
