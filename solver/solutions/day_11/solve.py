from solver.utils.file_utils import *
import os

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
  stars = get_stars_after_expand_galaxy(data)
  paths = get_shortest_paths_between_stars(stars)
  return sum(paths)

def solve_second_part(data):
  stars = get_stars_after_expand_galaxy(data, 1000000)
  paths = get_shortest_paths_between_stars(stars)
  return sum(paths)

def get_stars_after_expand_galaxy(data, expansion_rate = 1):
  rows_to_expand = []
  for i in range(len(data)):
    if all([char == '.' for char in data[i]]):
      rows_to_expand.append(i)
  
  cols_to_expand = []
  for i in range(len(data[0])):
    col = []
    for row in data:
      col.append(row[i])
    if all([char == '.' for char in col]):
      cols_to_expand.append(i)

  stars = []

  for x in range(len(data)):
    for y in range(len(data[x])):
      if data[x][y] == '#':
        stars.append((y, x))
  
  new_stars = []
  for star in stars:
    expanded_col_space = [col for col in cols_to_expand if col < star[0]]
    expanded_row_space = [row for row in rows_to_expand if row < star[1]]

    expansion_col = len(expanded_col_space)
    expansion_row = len(expanded_row_space)
    if (len(expanded_col_space) > 0 and expansion_rate > 1):
      expansion_col = (len(expanded_col_space) * expansion_rate) - len(expanded_col_space)

    if (len(expanded_row_space) > 0 and expansion_rate > 1):
      expansion_row = (len(expanded_row_space) * expansion_rate) - len(expanded_row_space)
    new_stars.append((star[0] + expansion_col, star[1] + expansion_row))
  
  return new_stars

def get_shortest_paths_between_stars(stars):
  paths = []
  for i in range(len(stars) - 1):
    j = i + 1
    while j <= len(stars) - 1:
      from_star = stars[i]
      to_star = stars[j]
      x_path = abs(to_star[0] - from_star[0])
      y_path = abs(to_star[1] - from_star[1])
      paths.append(x_path + y_path)
      j += 1
  return paths