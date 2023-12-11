from solver.utils.file_utils import *
import os

# Each contains array of tuple for x and y
pipe_move_modifiers = {
  '|': [(0, -1), (0, 1)],
  '-': [(-1, 0), (1, 0)],
  'L': [(0, -1), (1, 0)],
  'J': [(0, -1), (-1, 0)],
  '7': [(0, 1), (-1, 0)],
  'F': [(0, 1), (1, 0)],
  '.': [],
  'S': []
}

around_point_map = [(-1, 0), (0, -1), (1, 0), (0, 1)]

row_length = 0

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
  formatted_input = format_data(data)
  global row_length
  row_length = formatted_input['row_length']
  looped_pipes = get_looped_pipes(formatted_input)
  return get_furthers_pipe_by_steps(looped_pipes)
  pass


def solve_second_part(data):
  pass


def format_data(data):
  row_length = len(data[0])
  joined_rows = ''.join(data)
  pipes = []
  start_char_position = None
  for i in range(len(joined_rows)):
    raw_pipe = joined_rows[i]
    if raw_pipe == 'S':
      start_char_position = i
    pipe = {'type': raw_pipe, 'index': i, 'move_modifiers': pipe_move_modifiers[raw_pipe]}
    pipes.append(pipe)
  return {'row_length': row_length, 'pipes': pipes, 'start_position': start_char_position}


def get_x_y_coordinates(index):
  x = index % row_length
  y = (index - x) / row_length

  return (x, y)


def x_y_to_index(coordinates):
  return int(coordinates[0] + (coordinates[1] * row_length))


def move_index_by_move_modifier(index, move_modifier):
  x, y = get_x_y_coordinates(index)
  x, y = move_modifier[0] + x, move_modifier[1] + y
  return x_y_to_index((x, y))

def get_points_around_index(index):
  origin_point = get_x_y_coordinates(index)
  points_around = []
  for point in around_point_map:
    x, y = origin_point[0] + point[0], origin_point[1] + point[1]
    points_around.append(x_y_to_index((x, y)))

  return points_around


def get_looped_pipes(data):
  pipes = data['pipes']
  origin_index = data['start_position']
  points_around = get_points_around_index(origin_index)

  paths = []
  for point_around in points_around:
    is_connected = is_pipe_connected_to(pipes[point_around], pipes[origin_index])
    if is_connected:
      paths.append([pipes[origin_index], pipes[point_around]])

  looped_paths = [False for path in paths]
  loop_index = 0

  while not all(looped_paths):
    loop_index += 1
    for i in range(len(paths)):
      if looped_paths[i]:
        continue
      last_pipe = paths[i][-1]
      target_pipes_indexes = get_pipes_indexes_connected_to(last_pipe)
      not_repeated_pipes = [pipes[index] for index in target_pipes_indexes if pipes[index] not in paths[i]]
      if len(not_repeated_pipes) == 0:
        looped_paths[i] = True
      else:
        paths[i] += not_repeated_pipes

  return paths

def is_pipe_connected_to(pipe_from, pipe_to):
  for move_modifier in pipe_from['move_modifiers']:
    move_result = move_index_by_move_modifier(pipe_from['index'], move_modifier)
    if move_result == pipe_to['index']:
      return True
  return False

def get_pipes_indexes_connected_to(pipe):
  origin_point = pipe['index']
  move_modifiers = pipe['move_modifiers']

  target_indexes = []
  for move_modifier in move_modifiers:
    target_indexes.append(move_index_by_move_modifier(origin_point, move_modifier))
  return target_indexes

def get_furthers_pipe_by_steps(looped_pipes):
  for i in range(len(looped_pipes[0])):
    if i == 0:
      continue

    current_pipes = []
    for pipes in looped_pipes:
      current_pipes.append(pipes[i])
    
    are_all_same = [pipe == current_pipes[0] for pipe in current_pipes]

    if all(are_all_same):
      return i

    
