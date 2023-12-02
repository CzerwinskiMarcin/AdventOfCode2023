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
  data = remove_letters(data)
  numbers = []
  for line in data:
    numbers.append(get_value_from_line(line))
  
  return sum(numbers)

def solve_second_part(data):
  new_data = translate_words_to_numbers(data)
  debug = []
  for index in range(len(new_data)):
    debug.append('{}\n'.format(data[index]))
    debug.append('{}\n'.format(new_data[index]))
    debug.append('\n')

  return solve_first_part(new_data)

def remove_letters(data):
  new_data = []
  for line in data:
    new_data.append(re.sub(r'[a-zA-z]', '', line))
  
  return new_data

def translate_words_to_numbers(data):
  translate_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
  }

  new_data = []
  for line in data:
    line = str(line)

    first_word = None
    last_word = None
    first_word_index = len(line)
    last_word_index = -1 

    first_number_index = len(line)
    last_number_index = -1 

    for index, char in enumerate(line):
      if not char.isnumeric():
        continue

      if first_number_index > index:
        first_number_index = index
      if last_number_index < index:
        last_number_index = index

    for word in translate_map:
      new_first_index = line.find(word)
      new_last_index = line.rfind(word)

      if new_first_index >= 0 and first_word_index > new_first_index:
        first_word_index = new_first_index
        first_word = word
      if new_last_index >= 0 and last_word_index < new_last_index:
        last_word_index = new_last_index
        last_word = word

    if first_word and first_word_index < first_number_index:
      line = line.replace(first_word, translate_map[first_word], 1)
    
    if last_word and last_word_index > last_number_index:
      line = rreplace(line, last_word, translate_map[last_word], 1)

    new_data.append(line)

  return new_data

def get_value_from_line(line):
  if len(line) == 0:
    return 0
  if len(line) == 2:
    return int(line)
  else:
    first_letter = line[0]
    second_letter = line[-1]
    number = first_letter + second_letter
    return int(number)

def rreplace(s, old, new, occurence):
  li = s.rsplit(old, occurence)
  return new.join(li)
