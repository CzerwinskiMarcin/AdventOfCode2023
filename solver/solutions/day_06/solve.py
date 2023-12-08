from solver.utils.file_utils import *
import os
import re

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
  formatted_data = format_data(data)
  return count_winning_way_number(formatted_data)

def solve_second_part(data):
  formatted_data = format_data_second_part(data)
  return count_winning_way_number(formatted_data)

def format_data(data):
  [time_line, distance_line] = data
  times = [int(x) for x in re.findall(r'[0-9]+', time_line)]
  distances = [int(x) for x in re.findall(r'[0-9]+', distance_line)]
  formatted_data = []
  for i in range(len(times)): {
    formatted_data.append({'time': times[i], 'distance': distances[i]})
  }
  return formatted_data

def format_data_second_part(data):
  [time_line, distance_line] = data
  times = [x for x in re.findall(r'[0-9]+', time_line)]
  distances = [x for x in re.findall(r'[0-9]+', distance_line)]
  time = int(''.join(times))
  distance = int(''.join(distances))
  return [{'time': time, 'distance': distance}]

def count_winning_way_number(data):
  winning_ways = []
  for d in data:
    result = count_winning_possibilities(d['time'], d['distance'])
    winning_ways.append(result)

  multiplied_ways = None
  for way in winning_ways:
    if multiplied_ways == None:
      multiplied_ways = way
    else:
      multiplied_ways *= way
  return multiplied_ways

def count_winning_possibilities(time, distance):
  winning_possibilities = 0
  for t in range(time+1):
    distance_reached = t * (time - t)
    if distance_reached > distance:
      winning_possibilities += 1
  return winning_possibilities