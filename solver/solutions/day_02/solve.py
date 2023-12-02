from solver.utils.file_utils import *
import os
import re

first_part_max_cubes = {
  'red': 12,
  'green': 13,
  'blue': 14
}

def solve(type, part):
  target_data_file = 'test.txt' if type == 'test' else 'data.txt'
  solve_directory_path = os.path.dirname(__file__)
  filepath = os.path.join(solve_directory_path, 'data', target_data_file)
  data = read_lines(filepath)
  data = process_data(data)
  return do_solve(part, data)

def do_solve(part, data):
  if part == 'first':
    return solve_first_part(data)
  else:
    return solve_second_part(data)

def solve_first_part(data):
  filtered_games = filter_out_impossible_games(data, first_part_max_cubes)
  return calculate_sum_of_games_indexes(filtered_games)

def solve_second_part(data):
  minimum_rules = get_minimum_rules_for_games(data)
  return calculate_sum_of_games_set_powers(minimum_rules)

def process_data(data):
  games_data = []
  for line in data:
    raw_game_index, raw_game_data = line.split(':')
    game_data = {}
    game_data['index'] = re.sub(r'[a-zA-Z ]', '', raw_game_index)
    game_data['sets'] = process_game_data(raw_game_data)
    games_data.append(game_data)
  return games_data

def process_game_data(game_data):
  raw_sets = game_data.split('; ')
  sets_data = []
  for raw_set in raw_sets:
    cleaned_set_data = raw_set.replace(', ', '#').replace(' ', '').split('#')
    set_data = {}
    for set_part_data in cleaned_set_data:
      digit = re.search(r'[1234567890]*', set_part_data).group(0)
      color = re.sub(r'[1234567890 ]', '', set_part_data)
      set_data[color] = digit
    sets_data.append(set_data)
  return sets_data

def filter_out_impossible_games(games_data, rules):
  filtered_games = []
  for game in games_data:
    is_possible = True
    for set in game['sets']:
      for rule in rules:
        if int(set.get(rule, 0)) > int(rules[rule]):
          is_possible = False
          break
    if is_possible:
      filtered_games.append(game)
  return filtered_games

def calculate_sum_of_games_indexes(games_data):
  sum = 0
  for game in games_data:
    sum += int(game.get('index', 0))
  return sum

def get_minimum_rules_for_games(games_data):
  minimum_rules = []
  for game in games_data:
    rule = {'red': 0, 'green': 0, 'blue': 0}
    for set in game.get('sets'):
      for set_part in set:
        if rule[set_part] < int(set[set_part]):
          rule[set_part] = int(set[set_part])
    minimum_rules.append(rule)
  return minimum_rules

def calculate_sum_of_games_set_powers(rules):
  sum = 0
  for rule in rules:
    set_power = None
    for part in rule:
      if set_power == None:
        set_power = rule[part]
      else:
        set_power *= rule[part]
    sum += set_power
  return sum