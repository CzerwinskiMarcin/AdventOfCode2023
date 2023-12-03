from solver.utils.file_utils import *
import os
import re

around_positions_rel = {
  'lu': (-1, -1),
  'u': (0, -1),
  'ru': (1, -1),
  'l': (-1, 0),
  'r': (1, 0),
  'lb': (-1, 1),
  'b': (0, 1),
  'rb': (1, 1)
}

def solve(type, part):
  target_data_file = 'test.txt' if type == 'test' else 'data.txt'
  solve_directory_path = os.path.dirname(__file__)
  filepath = os.path.join(solve_directory_path, 'data', target_data_file)
  data = read_lines(filepath)
  return do_solve(part, data)

def do_solve(part, data):
  engine_schematic = '.'.join(data)
  line_length = len(data[0]) + 1
  data = {'engine_schematic': engine_schematic, 'line_length': line_length}
  if part == 'first':
    return solve_first_part(data)
  else:
    return solve_second_part(data)

def solve_first_part(data):
  symbol_positions = get_symbols_positions(data['engine_schematic'])
  numbers_data = get_numbers_and_positions(data['engine_schematic'])
  numbers_data_around_symbols = number_data_around_symbols(numbers_data, symbol_positions, data['line_length'])
  return calculate_sum_of_numbers(numbers_data_around_symbols)

def solve_second_part(data):
  gear_symbols_positions = get_symbols_positions(data['engine_schematic'], '[*]')
  numbers_data = get_numbers_and_positions(data['engine_schematic'])

  numbers = []
  for gear_symbol_position in gear_symbols_positions:
    numbers.append(number_data_around_symbols(numbers_data, [gear_symbol_position], data['line_length']))

  numbers = [number for number in numbers if len(number) == 2]
  ratios = calculate_ration_of_gears(numbers)
  return sum(ratios)

def get_symbols_positions(engine_schematic, symbols = '.'):
  positions = []
  search_string = '(?![1234567890.])' + symbols + '{1}'
  iterator = re.finditer(re.compile(search_string), engine_schematic)
  for pos in iterator:
    positions.append(pos.start())
  return positions

def get_numbers_and_positions(engine_schematic):
  numbers_data = []
  iterator = re.finditer(r'(?!^[10])*[1234567890]+', engine_schematic)
  for pos in iterator:
    data = {'number': pos.group(0), 'positions': (pos.start(), pos.end() - 1)}
    numbers_data.append(data)
  return numbers_data

def number_data_around_symbols(numbers_data, symbol_positions, line_length):
  number_close_to_symbols = []
  for symbol_position in symbol_positions:
    numbers_round_symbol_data = get_numbers_around_positions(numbers_data, symbol_position, line_length)
    for number in numbers_round_symbol_data:
      if number not in number_close_to_symbols:
        number_close_to_symbols.append(number)
  return number_close_to_symbols
  

def get_numbers_around_positions(numbers_data, position, line_length):
  numbers_around_position = []
  around_positions = get_around_position(position, line_length)
  for number in numbers_data:
    for position in around_positions:
      if number['positions'][0] <= position <= number['positions'][1] and number not in numbers_around_position:
        numbers_around_position.append(number)
        
  return numbers_around_position
  

def get_around_position(position, line_length): 
  around_positions = []
  for around_position_mod in around_positions_rel:
    around_position_rel = around_positions_rel[around_position_mod]
    around_positions.append(position + (around_position_rel[0] + (around_position_rel[1] * line_length)))
  return around_positions

def calculate_sum_of_numbers(numbers_data):
  numbers = [int(number['number']) for number in numbers_data]
  return sum(numbers)

def calculate_ration_of_gears(numbers_data):
  ratios = []
  for number_data in numbers_data:
    ratio = None
    for part in number_data:
      if ratio == None:
        ratio = int(part['number'])
      else:
        ratio *= int(part['number'])
    ratios.append(ratio)

  return ratios