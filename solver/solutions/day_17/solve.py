from solver.utils.file_utils import *
import os

movements = [(-1, 0, 'w'), (0, -1, 'n'), (1, 0, 'e'), (0, 1, 's')]

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
  length = len(data[0])
  height = len(data)
  tiles = format_data(data)
  path = find_path(tiles, length, height)

  last_path = path[-1]

  total_heat_loss = 0
  while last_path:
    print(last_path['index'], get_x_y_coordinates(last_path['index'], length), last_path['heat_loss'], last_path['directions_seq'])
    total_heat_loss += last_path['heat_loss']
    if 'parent' in last_path:
      last_path = last_path['parent']
    else:
      last_path = None
  return total_heat_loss

def solve_second_part(data):
  pass

def format_data(data):
  length = len(data[0])
  height = len(data)
  tiles = []
  for y in range(height):
    for x in range(length):
      index = x_y_to_index((x, y), length)
      # g is just heat loss
      tiles.append({'index': index, 'heat_loss': int(data[y][x]), 'g': int(data[y][x]), 'g_modifier': 1, 'directions_seq': ''})
  return tiles

# A* algorithm
def find_path(tiles, length, height):
  start_tile = tiles[0].copy()
  start_tile['f'] = 0
  open_list = [start_tile]
  closed_list = []
  goal_tile = tiles[-1].copy()
  goal_coordination = get_x_y_coordinates(goal_tile['index'], length)

  while len(open_list) > 0:
    q_node = get_tile_with_lowest_f_value(open_list)
    neightbour_tiles = get_neighbours_for_tile(q_node, tiles, length, height)
    closed_list.append(q_node)

    for tile in neightbour_tiles:
      if len(tile['directions_seq']) >= 3 and all(char == tile['directions_seq'][-1] for char in tile['directions_seq'][-3:]):
        continue

      if tile == tiles[-1]:
        closed_list.append(tile)
        return closed_list
      
      tile['g'] = q_node['g'] + tile['heat_loss'] * tile['g_modifier']
      tile_coordinate = get_x_y_coordinates(tile['index'], length)
      tile['h'] = abs(tile_coordinate[0] - goal_coordination[0]) + abs(tile_coordinate[1] + goal_coordination[1])
      tile['f'] = tile['h'] + tile['g']

      same_tile_in_open = [t for t in open_list if t['index'] == tile['index']]

      if len(same_tile_in_open) > 0:
        are_all_lower_f = all(t['f'] < tile['f'] for t in open_list)
        if are_all_lower_f:
          continue

      same_tile_in_closed = [t for t in closed_list if t['index'] == tile['index']]

      if len(same_tile_in_closed) > 0:
          are_all_lower_f = all(t['f'] < tile['f'] for t in closed_list)
          if are_all_lower_f:
            continue
      open_list.append(tile)

  return closed_list
      

def get_tile_with_lowest_f_value(tiles):
  lowest_tile = None
  for tile in tiles:
    if lowest_tile == None or lowest_tile['f'] > tile['f']:
      lowest_tile = tile
  tile_index_in_list = tiles.index(lowest_tile)
  return tiles.pop(tile_index_in_list)

def get_neighbours_for_tile(origin_tile, tiles, length, height):
  (x, y) = get_x_y_coordinates(origin_tile['index'], length)
  neighbour_tiles = []

  for movement in movements:
    new_x = x + movement[0]
    new_y = y + movement[1]

    if is_out_of_map((new_x, new_y), length, height):
      continue
    
    neightbour_tile = tiles[x_y_to_index((new_x, new_y), length)].copy()
    neightbour_tile['parent'] = origin_tile
    neightbour_tile['directions_seq'] = origin_tile['directions_seq'] + movement[2]
    neightbour_tile['g_modifier'] = 2 if all(char == movement[2] for char in neightbour_tile['directions_seq'][-3:]) else 1
    neighbour_tiles.append(neightbour_tile)

  return neighbour_tiles

def get_x_y_coordinates(index, row_length):
  x = index % row_length
  y = int((index - x) / row_length)
  return (x, y)

def x_y_to_index(coordinates, row_length):
  return int(coordinates[0] + (coordinates[1] * row_length))

def is_out_of_map(coordination, length, height):
  (x, y) = coordination
  is_out_on_x = x < 0 or x >= length
  is_out_on_y = y < 0 or y >= height
  
  return is_out_on_x or is_out_on_y