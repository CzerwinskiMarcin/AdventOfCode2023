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
  maps = get_maps(data)
  sources = get_seeds_ranges(data, maps)
  source_name = 'seed'

  destination_map = get_map(source_name, maps)

  while destination_map:
    # print('SOURCE NAME', source_name, '\n')
    new_sources = []
    for range in sources:
      ranges = get_destination_ranges(source_name, range, maps)
      mapped_ranges = get_mapped_ranges(ranges, destination_map)
      new_sources += mapped_ranges
    source_name = destination_map['destination']
    destination_map = get_map(source_name, maps)
    sources = new_sources
  
  # print('Final ranges')
  min = None
  for source in sources:
    if min == None or min > source['source_start']:
      min = source['source_start']
  return min


def get_seeds(data):
  return [int(seed_number) for seed_number in re.sub(r'seeds: ', '', data[0]).split(' ')]


def get_seeds_ranges(data, maps):
  seeds_data = [int(seed_number) for seed_number in re.sub(r'seeds: ', '', data[0]).split(' ')]
  seeds_formatted_data = []
  for source_start, source_range in zip(*[iter(seeds_data)]*2):
    seeds_formatted_data.append({'source_start': source_start, 'source_range': source_range})
  return seeds_formatted_data


def get_destination_ranges(source, source_range, maps):
  source_to_destination_map = get_map(source, maps)
  desitnation_ranges = source_to_destination_map['maps']
  affected_ranges = []
  for destination_range in desitnation_ranges:
    is_start_source_in_range = destination_range['source'] <= source_range['source_start'] <= destination_range['source'] + destination_range['range'] - 1
    is_end_source_in_range = destination_range['source'] <= source_range['source_start'] + source_range['source_range'] - 1 <= destination_range['source'] + destination_range['range'] - 1
    is_start_destination_in_source = source_range['source_start'] <= destination_range['source'] <= source_range['source_start'] + source_range['source_range'] - 1
    is_end_destination_in_source = source_range['source_start'] <= destination_range['source'] + destination_range['range'] - 1 <= source_range['source_start'] + source_range['source_range'] - 1
    # print('Source', source_range)
    # print('Destination', destination_range)
    # print(f"\tSource start between destination range \t\t{destination_range['source']} <= {source_range['source_start']} <= {destination_range['source'] + destination_range['range'] - 1}", is_start_source_in_range)
    # print(f"\tSource end between destination range \t\t{destination_range['source']} <= {source_range['source_start'] + source_range['source_range'] - 1} <= {destination_range['source'] + destination_range['range'] - 1}", is_end_source_in_range)
    # print(f"\tDestination start between source range \t\t{source_range['source_start']} <= {destination_range['source']} <= {source_range['source_start'] + source_range['source_range'] - 1}", is_start_destination_in_source)
    # print(f"\tDestination start between source range \t\t{source_range['source_start']} <= {destination_range['source'] + destination_range['range'] - 1} <= {source_range['source_start'] + source_range['source_range'] - 1}", is_end_destination_in_source)
    # print(f'Is destination affecting source {is_start_source_in_range or is_end_source_in_range or is_start_destination_in_source or is_end_destination_in_source}')
    # print()

    if is_start_source_in_range or is_end_source_in_range or is_start_destination_in_source or is_end_destination_in_source:
      affected_ranges.append({'destination': destination_range, 's_start': is_start_source_in_range, 's_end': is_end_source_in_range, 'd_start': is_start_destination_in_source, 'd_end': is_end_destination_in_source})

  return fill_ranges(source_range, affected_ranges)


def get_mapped_ranges(ranges, map):
  # print('\n\tget_mapped_ranges')
  mapped_ranges = []
  for range in ranges:
    mapped_start = get_mapped_value_for_map(range['source_start'], map)
    # print(f'\t\tOrigin start:\t{range["source_start"]}\tmapped to\t{mapped_start}')
    mapped_ranges.append({'source_start': mapped_start, 'source_range': range['source_range']})
  return mapped_ranges
    

def get_source(el):
  return el['destination']['source']


def fill_ranges(source_range, destination_ranges):
  ordered_destination_ranges = sorted(destination_ranges, key=get_source)
  index = source_range['source_start']
  limit_index = source_range['source_start'] + source_range['source_range']

  ranges = []
  next_destination_range = ordered_destination_ranges.pop() if len(ordered_destination_ranges) > 0 else None
  # print('Fill ranges for source_range:', source_range)
  # print(f'\tDestination ranges:', destination_ranges)
  # print('\tState of')
  # print(f'\tIndex: {index}')
  # print(f'\tLimit index: {limit_index}')

  while index < limit_index:
    # print('\t\tSource:', source_range)
    # print('\t\tDestination:', next_destination_range)
    # print('\t\tIndex:', index)
    # print('\t\tLimit index:', limit_index)

    if next_destination_range == None:
      # print(f'\t\t\t{get_source_destination_relation(next_destination_range)}')
      source_range = {'source_start': index , 'source_range': limit_index}
      index = limit_index
      
    elif next_destination_range['s_start'] and next_destination_range['s_end']:
      # print(f'\t\t\t{get_source_destination_relation(next_destination_range)}')
      index = source_range['source_start'] + source_range['source_range']

    elif next_destination_range['d_start'] and next_destination_range['d_end']:
      # print(f'\t\t\t{get_source_destination_relation(next_destination_range)}')
      if index == next_destination_range['destination']['source']:
        source_start = index
        range = next_destination_range['destination']['range']
        source_range = {'source_start': source_start, 'source_range': range}
        index = source_start + range

        if len(ordered_destination_ranges) > 0:
          next_destination_range = ordered_destination_ranges.pop()
        else:
          next_destination_range = None

      else:
        source_start = index
        range = next_destination_range['destination']['source'] - source_start
        source_range = {'source_start': source_start, 'source_range': range}
        index = source_start + range

    elif next_destination_range['s_start'] and next_destination_range['d_end']:
      # print(f'\t\t\t{get_source_destination_relation(next_destination_range)}')
      source_start = index
      range = next_destination_range['destination']['source'] + next_destination_range['destination']['range'] - source_start
      source_range = {'source_start': source_start, 'source_range': range}

      if len(ordered_destination_ranges) > 0:
        next_destination_range = ordered_destination_ranges.pop()
      else:
        next_destination_range = None

    elif next_destination_range['s_end'] and next_destination_range['d_start']:
      # print(f'\t\t\t{get_source_destination_relation(next_destination_range)}')
      if index < next_destination_range['destination']['source']:
        source_start = index
        range = next_destination_range['destination']['source'] - index
        source_range = {'source_start': source_start, 'source_range': range}
        index = next_destination_range['destination']['source']
        # print(f'\t\t\t\tAdding range to not filled place. Start: {source_start}, range: {range}')
      else:
        source_start = next_destination_range['destination']['source']
        # print(f'\t\t\t\tEnd of destination range: {source_start + next_destination_range["destination"]["range"]} < {limit_index}: {next_destination_range["destination"]["range"] < limit_index}')
        range = limit_index - source_start
        source_range = {'source_start': source_start, 'source_range': range}
        index = source_start + range
        # print(f'\t\t\t\tAdding range to for destination place. Start: {source_start}, range: {range}')
    
    # print('\t\tAdding source', source_range)
    # print()
    ranges.append(source_range)
  
  # print('\tRanges', ranges)

  return ranges


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
    source_map = get_map(source, maps)
    if source_map == None:
      is_last = True
      continue

    current_value = get_mapped_value_for_map(current_value, source_map)
    source = source_map['destination']

  return current_value


def get_mapped_value_for_map(value, map):
    ranges = get_ranges(value, map)

    if not ranges:
      return value

    return get_mapped_value(value, ranges)


def get_map(source, maps):
  source_map = [map for map in maps if map['source'] == source]
  if len(source_map) == 0:
    return None
  return source_map[0]


def get_ranges(value, map):
  for ranges in map['maps']:
    has_map = ranges['source'] <= value <= ranges['source'] + ranges['range']
    if has_map:
      return ranges
  return None


def get_mapped_value(value, ranges):
  offset = ranges['destination'] - ranges['source']
  return value + offset


def get_source_destination_relation(destination):
    if destination == None:
      return 'Not overlapping'
    elif destination['s_start'] and destination['s_end']:
      return 'Whole source is in destination range'
    elif destination['d_start'] and destination['d_end']:
      return 'Whole destination is in start range'
    elif destination['s_start'] and destination['d_end']:
      return 'Source start in range of destination range'
    elif destination['s_end'] and destination['d_start']:
      return 'Source end in range of destination range'