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
  remove_known_damaged_spring(formatted_data)
  count_possibility_of_damaged_springs(formatted_data)
  pass

def solve_second_part(data):
  pass

def format_data(data):
  formatted_data = []
  for line in data:
    [text_record, numbers_record] = line.split(' ')
    numbers = [int(number) for number in numbers_record.split(',')]
    chunked_text_records = re.sub(r'\.+', '|', text_record).split('|')
    text_records = [record for record in chunked_text_records if record != '']
    formatted_data.append({'text_records':text_records, 'numbers_records': numbers})
  return formatted_data

def remove_known_damaged_spring(formatted_data):
  for springs_row_data in formatted_data:
    text_records = springs_row_data['text_records']
    numbers_records = springs_row_data['numbers_records']
    text_records_indexes_to_delete = []
    numbers_record_indexes_to_delete = []
    for i in range(len(text_records)):
      if not all([spring == '#' for spring in text_records[i]]):
        continue
      for j in range(len(numbers_records)):
        if len(text_records[i]) != numbers_records[j]:
          continue
        if j >= i:
          text_records_indexes_to_delete.append(i)
          numbers_record_indexes_to_delete.append(j)
    text_records_indexes_to_delete.reverse()
    numbers_record_indexes_to_delete.reverse()
    text_records_indexes_to_delete = list(dict.fromkeys(text_records_indexes_to_delete))
    numbers_record_indexes_to_delete = list(dict.fromkeys(numbers_record_indexes_to_delete))

    for index in text_records_indexes_to_delete:
      del text_records[index]
    for index in numbers_record_indexes_to_delete:
      del numbers_records[index]
    
def count_possibility_of_damaged_springs(data):
  for records in data:
    text_records = records['text_records']
    numbers_records = records['numbers_records']
    offset = 0
    index = 0
    current_text_record = 0
    current_numbers_record = 0
    can_move_offset = True

    print(text_records)

    while can_move_offset:
      sequence_data = get_sequence_for_number_record(text_records[current_text_record], numbers_records[current_numbers_record], offset + index)
      new_index = sequence_data['end']

      print('\tNew loop')
      print('\tText sequence', text_records[current_text_record])
      print('\tIndex', index)
      print('\tNew index', new_index)
      print('\tOffset', offset)
      print('\tSequence data', sequence_data)

      print('\tIs next index out of range', index + 1 >= len(text_records[current_text_record]))

      index = new_index
      if index >= len(text_records[current_text_record]):
        print('\tMove offset one right:', offset + 1)
        index = 0
        offset += 1

      if offset >= len(text_records[current_text_record]):
        can_move_offset = False

      print('\tMove index one right:', index + 1)
      index += 1
      print()

      if index > 2:
        break

def get_sequence_for_number_record(text, number_record, offset):
  is_completed_sequence = False
  sequence = []
  index = 0 + offset
  print(f'\t\tSearching for number_record: {number_record} in "{text}"')
  while not is_completed_sequence:
    sequence.append(text[index])

    # Check if next char in text is damaged one
    if len(text) > index + 1 and text[index + 1] == "#":
      index += 1
      continue

    if len(text) <= index + 1:
      return None
    
    if len(sequence) >= number_record:
      print(f'\t\tFound sequence {sequence}, from: {offset} to {index}')
      return {'sequence': ''.join(sequence), 'start': offset, 'end': index}

  

    #   if offset < len(text_records[current_text_record]):
    #     print(f'\t{offset}')
    #     offset += 1
    #   elif len(text_records) > current_numbers_record + 1:
    #     print('\tNext text record')
    #     current_numbers_record += 1
    #     offset = 0
    #   elif len(numbers_records) > current_numbers_record + 1:
    #     print(f'\tNext numbers record')
    #     current_numbers_record += 1
    #   else:
    #     can_move_offset = False
    # print()
  
def count_even_possibilities(text_records, numbers_records):
  possibilities = 1
  for i in range(len(text_records)):
    possibilities *= len(text_records[i]) - numbers_records[i] + 1
  return possibilities

def count_odd_possibilities(text_records, numbers_records):
  for i in range(len(text_records)):
    print(text_records, numbers_records)
    clean_matching_from_string(text_records[i], numbers_records)

def clean_matching_from_string(text_record, numbers_records):
  for i in range(len(text_record)):
    last_sequence = ''
    matching_indexes = []

    while text_record[i] == '#':
      last_sequence += text_record[i]
      i += 1

    for j in range(len(numbers_records)):
      if numbers_records[j] == len(last_sequence):
        matching_indexes.append(j)

    
    if len(matching_indexes):
      print(matching_indexes)