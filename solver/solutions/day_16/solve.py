from solver.utils.file_utils import *
import os

movement_directions = {
  'north': (0, -1),
  'south': (0, 1),
  'west': (-1, 0),
  'east': (1, 0)
}

movement_modifier_elements = {
  '.': {
    'action': None
  },
  '/': {
    'action': 'change_direction',
    'data': [
    {'current_direction': 'north', 'to': 'east'},
    {'current_direction': 'west', 'to': 'south'},
    {'current_direction': 'south', 'to': 'west'},
    {'current_direction': 'east', 'to': 'north'}
    ]},
  '\\': {
    'action': 'change_direction',
    'data':[
    {'current_direction': 'north', 'to': 'west'},
    {'current_direction': 'east', 'to': 'south'},
    {'current_direction': 'south', 'to': 'east'},
    {'current_direction': 'west', 'to': 'north'}
  ]},
  '|': {
    'action': 'duplication',
    'data': [
      {'current_direction': 'east', 'to': 'south'},
      {'current_direction': 'east', 'to': 'north'},
      {'current_direction': 'west', 'to': 'north'},
      {'current_direction': 'west', 'to': 'south'}
    ]
  },
  '-': {
    'action': 'duplication',
    'data': [
      {'current_direction': 'north', 'to': 'west'},
      {'current_direction': 'north', 'to': 'east'},
      {'current_direction': 'south', 'to': 'west'},
      {'current_direction': 'south', 'to': 'east'}
    ]
  }
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
  formatted_data = format_data(data)
  beam = create_beam(0, 'east', False)
  length = formatted_data['length']
  height = formatted_data['height']
  tiles = formatted_data['tiles']
  return simulate_beam(beam, tiles.copy(), length, height)

def solve_second_part(data):
  formatted_data = format_data(data)
  length = formatted_data['length']
  height = formatted_data['height']
  tiles = formatted_data['tiles']
  top_tiles_data = [{'index': x_y_to_index((x, 0), length), 'initial_movement': 'south'} for x in range(length)]
  bottom_tiles_data = [{'index': x_y_to_index((x, height - 1), length), 'initial_movement': 'north'} for x in range(length)]
  left_side_tiles = [{'index': x_y_to_index((0, y), length), 'initial_movement': 'east'} for y in range(height)]
  right_side_tiles = [{'index': x_y_to_index((length - 1, y), length), 'initial_movement': 'west'} for y in range(height)]

  tiles_data = top_tiles_data + bottom_tiles_data + left_side_tiles + right_side_tiles

  largest_energization = 0

  for tile_data in tiles_data:
    copy_of_tiles = [copy_tile(tile) for tile in tiles]
    beam =  create_beam(tile_data['index'], tile_data['initial_movement'], False)
    result = simulate_beam(beam, copy_of_tiles, length, height)
    if largest_energization < result:
      largest_energization = result

  return largest_energization

def format_data(data):
  height = len(data)
  length = len(data[0])
  tiles_data = {
    'tiles': [],
    'length': length,
    'height': height
  }

  for i in range(height):
    for j in range(length):
      tile = {'index': x_y_to_index((j, i), length), 'type': data[i][j], 'energized': False, 'beams_passed': 0, 'from_directions': []}
      tiles_data['tiles'].append(tile)
  
  return tiles_data

def copy_tile(tile):
  new_tile = {}
  for key in tile:
    new_tile[key] = tile[key]
  new_tile['from_directions'] = []
  return new_tile

def simulate_beam(beam, tiles, length, height):
  beams = [beam]

  for beam in beams:
    out_of_map = False

    while not out_of_map:
      tile = tiles[beam['index']]
      new_beam = react_to_tile(beam, tile)
      if new_beam == beam:
        break
      elif new_beam != None:
        beams.append(new_beam)
      move_beam(beam, length, height)
      if beam['index'] == None:
        break
  return count_energized_tiles(tiles)

def create_beam(index, initial_movement, recently_created = True):
  return {'index': index, 'direction': initial_movement, 'recently_created': recently_created}

def move_beam(beam, length, height):
  (x, y) = get_x_y_coordinates(beam['index'], length)
  beam_direction = movement_directions[beam['direction']]
  x += beam_direction[0]
  y += beam_direction[1]
  if is_out_of_map((x, y), length, height) == True:
    beam['index'] = None
  else:
    new_index = x_y_to_index((x, y), length)
    beam['index'] = new_index

def react_to_tile(beam, tile):
  if beam['recently_created']:
    beam['recently_created'] = False
    return None

  tile['energized'] = True
  tile['beams_passed'] += 1

  if tile['type'] == '\\' or tile['type'] == '/':
    if beam['direction'] in tile['from_directions']:
      return beam

    tile['from_directions'].append(beam['direction'])
    movement_modifier = movement_modifier_elements[tile['type']]['data']
    target_movement_modifier = [modifier for modifier in movement_modifier if modifier['current_direction'] == beam['direction']][0]
    beam['direction'] = target_movement_modifier['to']
  elif tile['type'] == '|' or tile['type'] == '-':
    if beam['direction'] in tile['from_directions']:
      return beam


    tile['from_directions'].append(beam['direction'])
    movement_modifier = movement_modifier_elements[tile['type']]['data']
    target_movement_modifiers = [modifier for modifier in movement_modifier if modifier['current_direction'] == beam['direction']]

    if len(target_movement_modifiers) != 2:
      return None

    beam['direction'] = target_movement_modifiers[0]['to']
    new_beam = create_beam(beam['index'], target_movement_modifiers[1]['to'])
    return new_beam
  return None

def count_energized_tiles(tiles):
  return len([tile for tile in tiles if tile['energized']])

def is_out_of_map(coordination, length, height):
  (x, y) = coordination
  is_out_on_x = x < 0 or x >= length
  is_out_on_y = y < 0 or y >= height
  
  return is_out_on_x or is_out_on_y

def get_x_y_coordinates(index, row_length):
  x = index % row_length
  y = int((index - x) / row_length)
  return (x, y)

def x_y_to_index(coordinates, row_length):
  return int(coordinates[0] + (coordinates[1] * row_length))

def print_energized_map(tiles, length):
  sequence = ''
  for i in range(len(tiles)):
    if i % length == 0:
      print(sequence)
      sequence = ''
    sequence += '#' if tiles[i]['energized'] and tiles[i]['type'] == '.' else tiles[i]['type'] 
  print(sequence)
    
