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
  [rules, parts] = format_data(data)
  accepted_parts = get_accepted_parts(parts, rules)
  return sum_ratings(accepted_parts)

def solve_second_part(data):
  [rules, parts] = format_data(data)
  tree = create_paths_tree(rules)
  paths = get_path_from_a('A', tree)
  calculated = [calculate_path_combination(path, 'A', rules) for path in paths]
  return sum(calculated)

def format_data(data):
  are_raw_instructions = True
  rules = {}
  parts = []

  for line in data:
    if line == '':
      are_raw_instructions = False
      continue

    if are_raw_instructions:
      raw = re.sub(r'\}', '', line)
      [name, raw_rules] = raw.split('{')
      raw_rules = raw_rules.split(',')
      last_set = raw_rules.pop()

      r = []
      for raw_rule in raw_rules:
        [raw_rule, target_rule] = raw_rule.split(r':')
        [category, value] = re.split(r'[<>]', raw_rule)
        comparision = re.findall(r'[<>]', raw_rule)[0]
        r.append({'category': category, 'comparision': comparision, 'value': int(value), 'target': target_rule})
      r.append({'category': None, 'comparision': None, 'value': None, 'target': last_set})

      rules[name] = r

    else:
      raw_material_categories = re.sub(r'[\{\}]', '', line).split(r',')
      material = {}
      for material_category in raw_material_categories:
        [category, value] = material_category.split('=')
        material[category] = int(value)
      parts.append(material)

  return [rules, parts]

def get_accepted_parts(parts, clustered_rules):
  accepted_parts = []
  for part in parts:
    rule_name = 'in'

    while rule_name != 'A' and rule_name != 'R':
      rules = clustered_rules[rule_name]
      for i in range(len(rules)):
        if is_within_rule(part, rules[i]):
          rule_name = rules[i]['target']
          break
    
    if rule_name == 'A':
      accepted_parts.append(part)
  return accepted_parts
      

def is_within_rule(part, rule):
  category = rule['category']
  comparision = rule['comparision']
  target_value = rule['value']

  if comparision == None:
    return True
  if comparision == '<':
    return part[category] < target_value
  else:
    return part[category] > target_value

def sum_ratings(parts):
  sum = 0
  for part in parts:
    for key in part:
      sum += part[key]
  return sum

def get_reverse_paths_from_to(clustered_rules):
  current_target_node = 'A'

  while current_target_node != 'in':
    leading_rules = get_paths_with_target(current_target_node, clustered_rules)
    print(leading_rules)
    break

def get_paths_with_target(target, clustered_rules):
  rules_leading_to_target = []
  for rule_name in clustered_rules:
      if any([rule['target'] == 'A' for rule in clustered_rules[rule_name]]):
        rules_leading_to_target.append(rule_name)
  return rules_leading_to_target

def create_paths_tree(clustered_rules, entry_point = 'in'):
  root = {'label': entry_point, 'rule': clustered_rules[entry_point], 'parent': None, 'children': []}

  pending = [root]
  done = []

  while len(pending) > 0:
    current = pending.pop()
    children_rules = [rule for rule in current['rule']]

    for rule in children_rules:
      if rule['target'] == 'R' or rule['target'] == 'A':
        node = {'label': rule['target'], 'rule': None, 'parent': current, 'children': None}
        done.append(node)
        continue

      node = {'label': rule['target'], 'rule': clustered_rules[rule['target']], 'parent': current, 'children': []}
      current['children'].append(node)
      pending.append(node)
    
    done.append(current)
  return done

def get_path_from_a(target, tree):
  paths = []

  start_points = [node for node in tree if node['label'] == target]

  for point in start_points:
    path = [] 

    while point:
      path.append(point['label'])
      point = point['parent']
    path.reverse()
    paths.append(path)

  return paths

def calculate_path_combination(path, target, clustered_rules):
  combinations = []
  for i in range(len(path) - 1):
    current = path[i]
    next = path[i+1]
    print(current, next)

    rules = clustered_rules[current]
    for rule in rules:
      should_meet_rule = rule['target'] == next
      print(rule, should_meet_rule)
      if should_meet_rule:
        combinations.append(calculate_combinations_meeting_rule(rule))
      else:
        combinations.append(calculate_combinations_not_meeting_rule(rule))

      print(combinations[-1])

  print(combinations)
  print()
  distinct_combinations = 1

  for combination in combinations:
    distinct_combinations *= combination
  return distinct_combinations

def calculate_combinations_not_meeting_rule(rule):
  min = 1
  max = 4000
  comparision = rule['comparision']
  value = rule['value']

  if comparision == None:
    return 1
  elif comparision == '<':
    return max - value + 1
  else:
    return value
    
def calculate_combinations_meeting_rule(rule):
  min = 1
  max = 4000
  comparision = rule['comparision']
  value = rule['value']

  if comparision == None:
    return 1
  elif comparision == '<':
    return max - value - 1
  else:
    return value + 1