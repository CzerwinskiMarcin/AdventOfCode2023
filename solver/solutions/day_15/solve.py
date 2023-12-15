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
  return sum([hash_algorithm(text) for text in formatted_data])

def solve_second_part(data):
  formatted_data = format_data(data)
  instructions = get_lens_instructions(formatted_data)
  boxes = create_boxes()
  fill_boxes_with_lenses(instructions, boxes)
  return calculate_total_focus_power(boxes)

def format_data(data):
  return data[0].split(',')

def create_boxes():
  boxes = []
  for i in range(256):
    boxes.append([])
  return boxes

def fill_boxes_with_lenses(instructions, boxes):
  for instruction in instructions:
    if instruction['operation'] == '-':
      remove_lens_from_box(instruction, boxes)
      continue
    
    lens_with_label_in_box = is_lens_label_in_box(instruction, boxes)
    if lens_with_label_in_box:
      replace_lenses_in_box(lens_with_label_in_box, instruction, boxes)
    else:
      add_to_box(instruction, boxes)

def get_lens_instructions(formatted_data):
  instructions = []
  for raw_instruction in formatted_data:
    label = re.findall(r'[a-zA-z]+', raw_instruction)[0]
    operation = re.findall(r'[-|=]{1}', raw_instruction)[0]
    focal_length = re.findall(r'[0123456789]+', raw_instruction)
    focal_length = int(focal_length[0]) if len(focal_length) > 0 else None
    box = get_box_by_label(label)
    instructions.append({'label': label, 'operation': operation, 'focal_length': focal_length, 'box': box})
  return instructions
  
def get_box_by_label(label):
  return hash_algorithm(label)

def is_lens_label_in_box(lens_instruction, boxes):
  box = boxes[lens_instruction['box']]
  lenses_with_label = [lens for lens in box if lens['label'] == lens_instruction['label']]

  if len(lenses_with_label) > 1:
    raise IndexError

  return lenses_with_label[0] if len(lenses_with_label) else None

def replace_lenses_in_box(old_lens_instruction, new_lens_instruction, boxes):
  box = boxes[old_lens_instruction['box']]
  lens_index = boxes[old_lens_instruction['box']].index(old_lens_instruction)
  box[lens_index] = new_lens_instruction

def add_to_box(lens_instruction, boxes):
  boxes[lens_instruction['box']].append(lens_instruction)

def remove_lens_from_box(lens_instruction, boxes):
  box = boxes[lens_instruction['box']]
  for i in range(len(box)):
    if box[i]['label'] == lens_instruction['label']:
      del box[i]
      break

def hash_algorithm(text):
  current_value = 0

  for char in text:
    current_value += ord(char)
    current_value *= 17
    current_value %= 256

  return current_value

def calculate_total_focus_power(boxes):
  sum = 0
  for i in range(len(boxes)):
    for j in range(len(boxes[i])):
      lens_instruction = boxes[i][j]
      focal_length = lens_instruction['focal_length']
      box_factor = 1 + i
      slot_position_factor = j + 1
      sum += box_factor * slot_position_factor * focal_length
  return sum

def print_not_empty_boxes(boxes):
  filled_boxes = [box for box in boxes if len(box) > 0]
  for box in filled_boxes:
    print(box)
  print()
