from solver.utils.file_utils import *
import os
import re

def solve(type, part):
  target_data_file = 'test.txt' if type == 'test' else 'data.txt'
  solve_directory_path = os.path.dirname(__file__)
  filepath = os.path.join(solve_directory_path, 'data', target_data_file)
  data = read_lines(filepath)
  data = [d for d in data if d != '']
  return do_solve(part, data)

def do_solve(part, data):
  if part == 'first':
    return solve_first_part(data)
  else:
    return solve_second_part(data)

def solve_first_part(data):
  seeds = get_seeds(data)
  maps = get_maps(data)
  return min(get_last_values_from_maps(seeds, maps))

def solve_second_part(data):
  pass

def get_seeds(data):
  return [int(seed_number) for seed_number in re.sub(r'seeds: ', '', data[0]).split(' ')]

def get_maps(data):
  maps = []
  particular_map = {'source': None, 'destination': None, 'maps': []}
  for raw_map in data[1:]:
    if '-to-' in raw_map:
      if particular_map['source'] != None:
        maps.append(particular_map)
        particular_map = {'source': None, 'destination': None, 'maps': []}
      [source, target] = raw_map.replace(' map:', '').split('-to-')
      particular_map['source'] = source
      particular_map['destination'] = target
    else:
      [destination_start, source_start, range_length] = [int(number) for number in raw_map.split(' ')]
      range_map = {'source': source_start, 'destination': destination_start, 'range': range_length}
      particular_map['maps'].append(range_map)
  if particular_map['source'] != None:
        maps.append(particular_map)
  return maps

def get_last_values_from_maps(seeds, maps):
  values = []
  for seed in seeds:
    values.append(get_value_for_seed(seed, maps))
  return values
    

def get_value_for_seed(seed, maps):
  source = 'seed'
  is_last = False
  current_value = seed

  while not is_last:
    source_map = [map for map in maps if map['source'] == source]

    if len(source_map) == 0:
      is_last = True
      continue

    source_map = source_map[0]
    ranges = get_ranges(current_value, source_map)

    if not ranges:
      source = source_map['destination']
      continue

    current_value = get_mapped_value(current_value, ranges)
    source = source_map['destination']

  return current_value

def get_ranges(value, map):
  for ranges in map['maps']:
    has_map = ranges['source'] <= value <= ranges['source'] + ranges['range']
    if has_map:
      return ranges
  return None

def get_mapped_value(value, ranges):
  offset = ranges['destination'] - ranges['source']
  return value + offset